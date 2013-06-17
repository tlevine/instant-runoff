import re

import nose.tools as n

import instant_runoff as ir

def test_txt():
    'The text email should be generated as expected.'
    expected = open('fixtures/README.txt').read()
    input = open('fixtures/README.groff').read()
    observed = ir.groff_txt(input)
    n.assert_list_equal(observed.split('\n'), expected.split('\n'))

def test_html():
    'The HTML email should be generated as expected.'
    expected = open('fixtures/README.html').read()
    input = open('fixtures/README.groff').read()
    observed = ir.groff_html(input)
    n.assert_list_equal(observed.split('\n'), expected.split('\n'))

def test_eml():
    'The resulting multipart email should be generated as expected.'
    expected = open('fixtures/README.eml').read()
    input = open('fixtures/README.groff').read()

    def standardize_boundary(eml):
        return re.sub(r'===============[0-9]{19}==', ('=' * 17) + ('0' * 19) + '==', eml)

    observed = ir.compose(input).as_string()

    these = [standardize_boundary(eml).split('\n') for eml in [observed, expected]]
    n.assert_list_equal(*these)
