from gprofiler import gprofiler

def test_enrichment_call():
    enrichment = gprofiler(['Klf4', 'Pax5', 'Sox2', 'Nanog'], organism='mmusculus')
    assert enrichment is not None
