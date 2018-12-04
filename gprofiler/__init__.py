''' Python port of g:ProfileR, the R wrapper for the g:Profiler functional enrichment tool.
'''

import requests
import pandas as pd

BASE_URL = "http://biit.cs.ut.ee/gprofiler/"
HEADERS = {'User-Agent': 'python-gprofiler'}

def gprofiler(query, organism='hsapiens', ordered_query=False, significant=True,
              exclude_iea=False, region_query=False, max_p_value=1.0, max_set_size=0,
              correction_method='analytical', hier_filtering='none',
              domain_size='annotated', custom_bg=[], numeric_ns='', no_isects=False,
              png_fn=None, include_graph=False, src_filter=None):
    ''' Annotate gene list functionally

    Interface to the g:Profiler tool for finding enrichments in gene lists. Organism
    names are constructed by concatenating the first letter of the name and the
    family name. Example: human - 'hsapiens', mouse - 'mmusculus'. If requesting PNG
    output, the request is directed to the g:GOSt tool in case 'query' is a vector
    and the g:Cocoa (compact view of multiple queries) tool in case 'query' is a
    list. PNG output can fail (return FALSE) in case the input query is too large.
    In such case, it is advisable to fall back to a non-image request.

    Returns a pandas DataFrame with enrichment results

    '''
    query_url = ''
    my_url = BASE_URL + 'gcocoa.cgi'
    wantpng = True if png_fn else False
    output_type = 'mini_png' if wantpng else 'mini'

    if wantpng:
        raise NotImplementedError('PNG Output not implemented')
        return

    if include_graph:
        raise NotImplementedError('Biogrid Interactions not implemented (include_graph)')
        return

    # Query

    qnames = list(query)

    if len(qnames) == 0:
        raise ValueError('Missing query')
        return

    query_url = ' '.join(qnames)

    # Significance threshold

    if correction_method == 'gSCS':
        correction_method = 'analytical'

    if correction_method not in ('analytical', 'fdr', 'bonferroni'):
        raise ValueError("Multiple testing correction method not recognized (correction_method)")
        return

    # Hierarchical filtering

    if hier_filtering not in ('none', 'moderate', 'strong'):
        raise ValueError("hier_filtering must be one of \"none\", \"moderate\" or \"strong\"")
        return

    if hier_filtering == 'strong':
        hier_filtering = 'compact_ccomp'
    elif hier_filtering == 'moderate':
        hier_filtering = 'compact_rgroups'
    else:
        hier_filtering = ''

    # Domain size

    if domain_size not in ('annotated', 'known'):
        raise ValueError("domain_size must be one of \"annotated\" or \"known\"")
        return

    # Custom background

    if type(custom_bg) == list:
        custom_bg = ' '.join(custom_bg)
    else:
        raise TypeError('custom_bg need to be a list')
        return

    # Max. set size

    if max_set_size < 0:
        max_set_size = 0

    # HTTP request

    query_params = {
        'organism': organism,
        'query': query_url,
        'output': output_type,
        'analytical': '1',
        'sort_by_structure': '1',
        'ordered_query': '1' if ordered_query else '0',
        'significant': '1' if significant else '0',
        'no_iea': '1' if exclude_iea else '0',
        'as_ranges': '1' if region_query else '0',
        'omit_metadata': '0' if include_graph else '1',
        'user_thr': str(max_p_value),
        'max_set_size': str(max_set_size),
        'threshold_algo': correction_method,
        'hierfiltering': hier_filtering,
        'domain_size_type': domain_size,
        'custbg_file': '',
        'custbg': custom_bg,
        'prefix': numeric_ns,
        'no_isects': '1' if no_isects else '0'
    }

    if src_filter:
        for i in src_filter:
            query_params['sf_' + i] = '1'


    raw_query = requests.post(my_url, data=query_params, headers=HEADERS)

    # Here PNG request parsing would go, but not implementing that

    if wantpng:
        pass

    # Requested text

    split_query = raw_query.text.split('\n')

    commented_lines = filter(lambda s: s.startswith('#'), split_query)

    # Here interaction parsing would go, but not implementing that

    if include_graph:
        pass

    # Parse main result body

    split_query = filter(lambda s: not s.startswith('#'), split_query)
    split_query = filter(lambda s: not len(s) == 0, split_query)
    split_query = map(lambda s: s.split('\t'), split_query)
        
    enrichment = pd.DataFrame(list(split_query))
    if (enrichment.shape[1]>0):
        enrichment.columns = ["query.number", "significant", "p.value", "term.size",
                          "query.size", "overlap.size", "recall", "precision",
                          "term.id", "domain", "subgraph.number", "term.name",
                          "relative.depth", "intersection"]
        enrichment.index = enrichment['term.id']
        numeric_columns = ["query.number", "p.value", "term.size",
                       "query.size", "overlap.size", "recall", "precision",
                       "subgraph.number", "relative.depth"]
        for column in numeric_columns:
            enrichment[column] = pd.to_numeric(enrichment[column])

        enrichment['significant'] = enrichment['significant'] == '!'
    else:
        enrichment=list()

    return enrichment

