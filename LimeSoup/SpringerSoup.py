#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import re

from LimeSoup.lime_soup import Soup, RuleIngredient
from LimeSoup.parser.parser_paper_springer import ParserPaper


__author__ = 'Alex van Grootel'
__maintainer__ = 'Alex van Grootel'
__email__ = 'agrootel@mit.edu'
__version__ = '0.3.0'


class SpringerFindJournalName(RuleIngredient):
    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = [
            {'name': 'i', 'data-test':'journal-title'}
        ]
        try:
            ParserPaper.journal_name = next(x for x in parser.get(rules))
        except StopIteration:
            ParserPaper.journal_name = None
        return parser.raw_html


class SpringerRemoveTagsSmallSub(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        """
        Deal with spaces in the sub, small tag and then remove it.
        """
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = [
                 {'name': 'sub'},
                 {'name': 'sup'},
                 {'name': 'em', 'class': re.compile("EmphasisTypeItalic *")}, 
                 {'name': 'strong', 'class': re.compile("EmphasisTypeBold *")},
                 {'name': 'div', 'class':'Equation EquationMathjax'},
                 {'name': 'span', 'class':'InlineEquation'},
                 {'name': 'span', 'class':'InternalRef'}
                ]
        parser.operation_tag_remove_space(rules)
        # Remove some specific all span that are inside of a paragraph 'p'
        parser.strip_tags(rules)
        tags = parser.soup.find_all(**{'name': 'p'})
        parser.strip_tags(rules)
        html_str = str(parser.soup)
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)

        return parser.raw_html


class SpringerRemoveTrash(RuleIngredient):
    @staticmethod
    def _parse(html_str):
        # Tags to be removed from the HTML paper 
        list_remove = [
            {'name': 'div', 'class': 'Table'},  # Table
            {'name': 'div', 'class': 'HeaderArticleNotes'},  # submitted date
            {'name': 'p', 'class': 'skip-to'}, # Navigation links
            {'name': 'header', 'class': 'header u-interface'}, #search
            {'name': 'p', 'class': 'icon--meta-keyline-before'}, #published date and info
            {'name': 'h2', 'class': 'Heading u-jsHide'}, #Authors title
            {'name': 'li', 'class': 'c-article-author-list__item'}, #Authors
            {'name': 'div', 'class': 'article-context__container'}, #article context
            {'name': 'div', 'class': 'banner'}, #search
            {'name': 'aside', 'class': 'article-complementary-left'}, #Journal images
            {'name': 'figure', 'class': 'Figure'}, #Figures
            {'name': 'div', 'class': 'c-article-section__figure'}, #Figures
            {'name': 'aside', 'class': 'article-about'}, #About paper
            {'name': 'aside', 'class': 'article-complementary-right u-interface'}, #Article actions
            {'name': 'footer', 'class': 'footer'}, #Article footer
            {'name': 'div', 'class': 'ArticleCopyright content'}, #Copyright
            {'name': 'h2', 'id': 'copyrightInformation'}, #copyright title
            {'name': 'div', 'class': 'Acknowledgments'}, #Acknowledgements
            {'name': 'aside', 'class': 'Bibliography'}, #Acknowledgements
            {'name': 'section', 'id':'Notes'}, #acknowledgements
            {'name': 'span', 'class': 'CitationRef'}, #references
            {'name': 'div', 'id': 'rightslink-section'}, #Rights and permissions 
            {'name': 'div', 'id': 'author-information-section'}, #Author Information
            {'name': 'div', 'id': 'notes-content'}, #Notes
            {'name': 'div', 'id': 'Bib1-content'}, #Reference
            {'name': 'div', 'id': 'Ack1-content'}, #Acknowledgments
            {'name': 'div', 'data-component': 'share-box'}, #About this article
            {'name': 'div', 'id': 'article-info-content'}, #About this article
            {'name': 'div', 'id': 'ethics-section'}, #Ethics declarations
            {'name': 'div', 'id': 'additional-information-section'}, #Additional information
            {'name': 'section', 'data-title': 'Electronic supplementary material'}, #Electronic supplementary material
            {'name': 'section', 'data-title': 'Electronic Supplementary Material'}, #Electronic supplementary material
            {'name': 'section', 'data-title': 'Supplementary Information'}, #Supplementary Information
            
        ]
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.remove_tags(rules=list_remove)
        parser.remove_tag(
            rules=[{'name': 'p', 'class': 'bold italic', 'string': parser.compile('First published on')}]
        )
        return parser.raw_html

class SpringerCreateTags(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        # This create a standard of sections tag name
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.create_tag_sections()
        return parser.raw_html


class SpringerCreateTagAbstract(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        # Create tag from selection function in ParserPaper
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        parser.create_tag_from_selection(
            rule={'name': 'div', 'id': 'Abs1-content'},
            name_new_tag='h2'
        )
        return parser.raw_html


class SpringerReplaceDivTag(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = [{'name': 'div'}]
        parser.strip_tags(rules)
        rules = [{'name': 'span', 'id': parser.compile('^sect[0-9]+$')}]  # some span are heading
        _ = parser.strip_tags(rules)
        return parser.raw_html

class SpringerReplaceDivTagPara(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        rules = {'name': 'div', 'class': 'Para'}
        parser.rename_tag(rules, 'p')
        return parser.raw_html

class SpringerCollect(RuleIngredient):

    @staticmethod
    def _parse(html_str):
        parser = ParserPaper(html_str, parser_type='html.parser', debugging=False)
        # Collect information from the paper using ParserPaper
        parser.get_keywords(rules=[{'name': 'li', 'class': 'c-article-subject-list__subject'}])
        parser.get_title(rules=[
                {'name': 'h1', 'class' :'c-article-title', 'recursive': True},
            ]
        )
        # Create tag from selection function in ParserPaper
        data = list()
        
        parser.deal_with_sections()
        data = parser.data_sections
        
        obj = {
            'DOI': '',
            'Title': parser.title,
            'Keywords': parser.keywords,
            'Journal': ParserPaper.journal_name,
            'Sections': data
        }

        return obj

"""
Error where the paper has paragraphs (content) that is not inside of a tag,
problem to recover these paragraphs. 
"""
SpringerSoup = Soup(parser_version=__version__)
SpringerSoup.add_ingredient(SpringerRemoveTagsSmallSub())
SpringerSoup.add_ingredient(SpringerFindJournalName())
SpringerSoup.add_ingredient(SpringerCreateTagAbstract())
SpringerSoup.add_ingredient(SpringerRemoveTrash())
SpringerSoup.add_ingredient(SpringerCreateTags())
SpringerSoup.add_ingredient(SpringerReplaceDivTagPara())
SpringerSoup.add_ingredient(SpringerCollect())
