Python port of g:ProfileR, the R wrapper for the g:Profiler functional
enrichment tool.

Just like the R wrapper, it simply sends an HTTP request to
http://biit.cs.ut.ee/gprofiler/ and parses the text-only version of the
results.

You can simply install python-gprofiler by doing

	pip install gprofiler

It requires `requests` and `pandas`.

The ability to fetch a `.png` representation of the results is not implemented
as I don't see a use for it. Biogrid interaction graphs are also not parsed
since I never use those and am not sure how to parse them correctly.

Once the package is installed, here is an example of what to expect when running it in IPython:

	In [1]: from gprofiler import gprofiler

	In [2]: enrichment = gprofiler(['Klf4', 'Pax5', 'Sox2', 'Nanog'], organism='mmusculus')

	In [3]: enrichment.sort('p.value').head()
	Out[3]: 
	            query.number significant   p.value  term.size  query.size  \
	term.id                                                                 
	GO:0032526             1        True  0.000100         78           4   
	GO:0000976             1        True  0.000210        549           4   
	GO:0048598             1        True  0.000258        578           4   
	GO:0044212             1        True  0.000519        688           4   
	GO:0000975             1        True  0.000531        692           4   

	            overlap.size  recall  precision     term.id domain  \
	term.id                                                          
	GO:0032526             3    0.75      0.038  GO:0032526     BP   
	GO:0000976             4    1.00      0.007  GO:0000976     MF   
	GO:0048598             4    1.00      0.007  GO:0048598     BP   
	GO:0044212             4    1.00      0.006  GO:0044212     MF   
	GO:0000975             4    1.00      0.006  GO:0000975     MF   

	            subgraph.number  \
	term.id                       
	GO:0032526                9   
	GO:0000976                6   
	GO:0048598                2   
	GO:0044212                6   
	GO:0000975                6   

	                                                    term.name  relative.depth  \
	term.id                                                                         
	GO:0032526                          response to retinoic acid               2   
	GO:0000976        transcription regulatory region sequence...               4   
	GO:0048598                            embryonic morphogenesis               1   
	GO:0044212        transcription regulatory region DNA binding               3   
	GO:0000975                      regulatory region DNA binding               2   

	                    intersection  
	term.id                           
	GO:0032526       KLF4,NANOG,SOX2  
	GO:0000976  KLF4,NANOG,PAX5,SOX2  
	GO:0048598  KLF4,NANOG,PAX5,SOX2  
	GO:0044212  KLF4,NANOG,PAX5,SOX2  
	GO:0000975  KLF4,NANOG,PAX5,SOX2
