import nose.tools as n

import instant_runoff as ir

def test_txt():
    expected = open('fixtures/README.txt').read()
    input = open('fixtures/README.groff').read()
    observed = ir.groff_txt(input)
    n.assert_list_equal(observed.split('\n'), expected.split('\n'))

def test_html():
    expected = open('fixtures/README.html').read()
    input = open('fixtures/README.groff').read()
    observed = ir.groff_html(input)
    n.assert_list_equal(observed.split('\n'), expected.split('\n'))
