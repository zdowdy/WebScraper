from scraper import _parse

def test_parse_extracts_product_data():
    sample_html = '''
    <script>
    var __initialState__={"Products":[{"IsCombo":false,"SponsoredMsg":null,"ProductNumber":"20-331-858","ItemCell":{"Description":{"ProductName":"Test RAM 16GB"},"Model":"TEST123","ItemManufactory":{"Manufactory":"TestBrand"},"FinalPrice":99.99,"Review":{"RatingOneDecimal":4.5,"HumanRating":100},"Instock":true}}]};
    </script>
    '''
    
    results = _parse(sample_html)
    
    assert len(results) == 1
    assert results[0]['title'] == 'Test RAM 16GB'
    assert results[0]['brand'] == 'TestBrand'
    assert results[0]['price'] == 99.99