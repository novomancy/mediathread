from lettuce.django import django_url
from lettuce import before, after, world, step
import sys, time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from mediathread.projects.models import Project
from urlparse import urlparse

@step(u'There are no projects')
def there_are_no_projects(step):
    assert len(Project.objects.all()) == 0

@step(u'there is an? ([^"]*) ([^"]*) panel')
def there_is_a_state_name_panel(step, state, name):
    """
    Keyword arguments:
    state -- open, closed
    name -- composition, assignment, discussion, collection 

    """
    try:
        panel = world.firefox.find_element_by_css_selector("td.panel-container.%s.%s" % (state.lower(), name.lower()))
    except:
        time.sleep(1)
        panel = world.firefox.find_element_by_css_selector("td.panel-container.%s.%s" % (state.lower(), name.lower()))
    assert panel != None, "Can't find panel named %s" % panel
    
@step(u'there is not an? ([^"]*) ([^"]*) panel')
def there_is_not_a_state_name_panel(step, state, name):
    """
    Keyword arguments:
    state -- open, closed
    name -- composition, assignment, discussion, collection 

    """
    try:
        panel = world.firefox.find_element_by_css_selector("td.panel-container.%s.%s" % (state.lower(), name.lower()))
        assert False, "Found panel named %s" % panel
    except:
        pass # expected

@step(u'the ([^"]*) panel has an? ([^"]*) subpanel')
def the_name_panel_has_a_state_subpanel(step, name, state):
    panel = world.firefox.find_element_by_css_selector("td.panel-container.open.%s" % name.lower())
    assert panel != None, "Can't find panel named %s" % panel
    
    selector = "td.panel-container.%s" % state
    subpanel = panel.find_element_by_css_selector(selector)
    assert selector != None, "Can't find %s subpanel in %s panel" % (state, name)
    
@step(u'the ([^"]*) panel has an? ([^"]*) button')
def the_panel_has_a_name_button(step, panel, name):
    panel = world.firefox.find_element_by_css_selector("td.panel-container.open.%s" % panel.lower())
    assert panel != None, "Can't find panel named %s" % panel
    
    btn = world.find_button_by_value(name, panel)
    assert btn != None, "Can't find button named %s" % name
    
@step(u'the ([^"]*) panel does not have an? ([^"]*) button')
def the_panel_does_not_have_a_name_button(step, panel, name):
    panel = world.firefox.find_element_by_css_selector("td.panel-container.open.%s" % panel.lower())
    assert panel != None, "Can't find panel named %s" % panel
    
    try:
        btn = world.find_button_by_value(name, panel)
        assert False, "Found a button named %s" % name
    except:
        pass # expected
    
@step(u'I call the ([^"]*) "([^"]*)"')
def i_call_the_panel_title(step, panel, title):
    try:
        panel = world.firefox.find_element_by_css_selector("td.panel-container.open.%s" % panel.lower())
    except:
        time.sleep(1)
        panel = world.firefox.find_element_by_css_selector("td.panel-container.open.%s" % panel.lower())
    assert panel != None, "Can't find panel named %s" % panel
    
    input = panel.find_element_by_name("title")
    input.clear()
    input.send_keys(title)
    
@step(u'The ([^"]*) title is "([^"]*)"')
def the_panel_title_is_value(step, panel, value):
    try:
        panel = world.firefox.find_element_by_css_selector("td.panel-container.open.%s" % panel.lower())
    except:
        time.sleep(1)
        panel = world.firefox.find_element_by_css_selector("td.panel-container.open.%s" % panel.lower())
    assert panel != None, "Can't find panel named %s" % panel
    
    h1 = panel.find_element_by_css_selector("h1.project-title")
    assert h1.text.strip() == value, "Expected %s title %s. Found %s" % (panel, value, h1.text.strip())
        
@step(u'I write some text for the ([^"]*)')
def i_write_some_text_for_the_panel(step, panel):
    panel = world.firefox.find_element_by_css_selector("td.panel-container.open.%s" % panel.lower())
    assert panel != None, "Can't find panel named %s" % panel
    
    frame = panel.find_element_by_tag_name("iframe")
    world.firefox.switch_to_frame(frame)
    input = world.firefox.find_element_by_class_name("mceContentBody")
    input.send_keys("""The Columbia Center for New Teaching and Learning was (CCNMTL)
                    was founded at Columbia University in 1999 to enhance teaching and
                    learning through the purposeful use of new media and technology""")
    
    world.firefox.switch_to_default_content()
    
@step(u'I see a ([^"]*) dialog')
def i_see_a_name_dialog(step, name):
    elt = world.firefox.find_element_by_css_selector('span.ui-dialog-title')
    assert elt != None and elt.text == name
    
@step(u'the project visibility is "([^"]*)"')
def the_project_visibility_is_level(step, level):
    elt = world.firefox.find_element_by_css_selector("input[name=publish]:checked")
    assert elt != None
    
    label_selector = "label[for=%s]" % elt.get_attribute("id")
    label = world.firefox.find_element_by_css_selector(label_selector)
    if label.text.strip() == level:
        return

    assert False, "The %s option is not checked" % (level)
    
@step(u'There is a project visibility "([^"]*)"')
def there_is_a_project_visibility_level(step, level):
    elts = world.firefox.find_elements_by_name("publish")
    assert len(elts) > 0
    
    for e in elts:
        label_selector = "label[for=%s]" % e.get_attribute("id")
        label = world.firefox.find_element_by_css_selector(label_selector)
        if label.text.strip() == level:
            return

    assert False, "No %s option found" % (level)
    
@step(u'There is not a project visibility "([^"]*)"')
def there_is_not_a_project_visibility_level(step, level):
    elts = world.firefox.find_elements_by_name("publish")
    assert len(elts) > 0
    
    for e in elts:
        label_selector = "label[for=%s]" % e.get_attribute("id")
        label = world.firefox.find_element_by_css_selector(label_selector)
        if label.text.strip() == level:
            assert False, "Found %s option" % (level)    
    
@step(u'Then I set the project visibility to "([^"]*)"')
def i_set_the_project_visibility_to_level(step, level):
    elts = world.firefox.find_elements_by_name("publish")
    assert len(elts) > 0
    
    for e in elts:
        label_selector = "label[for=%s]" % e.get_attribute("id")
        label = world.firefox.find_element_by_css_selector(label_selector)
        if label.text.strip() == level:
            e.click()
            return

    assert False, "No %s option found" % (level)
    
@step(u'I select ([^"]*)\'s response')
def i_select_username_s_response(step, username):
    elt = world.firefox.find_element_by_name("responses")
    
    select = Select(elt)
    for o in select.options:
        if o.text.find(username) > -1:
            select.select_by_visible_text(o.text)
            return
    assert False, "Unable to find a response for %s" % username

  
     
    
@step(u'i save the changes')
def i_save_the_changes(step):
    elts = world.firefox.find_elements_by_tag_name("button")
    for e in elts:
        if e.get_attribute("type") == "button" and e.text == "Save":
            e.click()
            time.sleep(1)
            return
        
    assert False, "Unable to locate the dialog's save button"
    
@step(u'there is an? ([^"]*) "([^"]*)" project by ([^"]*)')
def there_is_a_status_title_project_by_author(step, status, title, author):
    elts = world.firefox.find_elements_by_css_selector("li.projectlist")
    if len(elts) < 1:
        time.sleep(1)
        elts = world.firefox.find_elements_by_css_selector("li.projectlist")
    assert len(elts) > 0, "Expected to find at least 1 project. Instead there are none"
    
    assignment = False
    for e in elts:
        try:
            title_elt = e.find_element_by_css_selector("a.asset_title.type-project")
        except:
            title_elt = e.find_element_by_css_selector("a.asset_title.type-assignment")
            assignment = True
            
        if title_elt.text.strip() == title:
            if not assignment:
                # author
                author_elt = e.find_element_by_css_selector("span.metadata-value-author")
                msg = "%s author is [%s]. Expected [%s]." % (title, author_elt.text.strip(), author)
                assert author_elt.text.strip() == author, msg
                
            # status            
            status_elt = e.find_element_by_css_selector("span.metadata-value-status")
            msg = "%s status starts with [%s]. Expected [%s]" % (title, status_elt.text.strip().lower(), status)
            assert status_elt.text.strip().lower().startswith(status), msg 
            
            return
            
    assert False, "Unable to find project named %s" % title
    
    
@step(u'there is a comment that begins "([^"]*)"')
def there_is_a_comment_that_begins_text(step, text):
    elts = world.firefox.find_elements_by_css_selector("div.threaded_comment_text")
    assert len(elts) > 0, "Expected to find at least one div.threaded_comment_text. Found 0"
    
    for e in elts:
        if e.text.startswith(text):
            return
        
    time.sleep(1)

    elts = world.firefox.find_elements_by_css_selector("div.threaded_comment_text")
    for e in elts:
        if e.text.startswith(text):
            return
    
    assert False, "Could not find a comment that begins with %s" % text
    
@step(u'I insert "([^"]*)" into the text')
def i_insert_title_into_the_text(step, title):
    link = world.firefox.find_element_by_partial_link_text(title)
    href = link.get_attribute("href")
    
    # strip the http://localhost:port off this href
    pieces = urlparse(href)
    
    
    insert_icon = world.firefox.find_element_by_name(pieces.path)
    insert_icon.click()

@step(u'Then I remember the "([^"]*)" link')
def then_i_remember_the_title_link(step, title):
    link = world.firefox.find_element_by_partial_link_text(title)
    world.memory[title] = link.get_attribute('href')

@step(u'I navigate to the "([^"]*)" link')
def i_navigate_to_the_title_link(step, title):
    link = world.memory[title]
    world.firefox.get(link)
    del(world.memory[title])
    

@step(u'I click the "([^"]*)" citation in the ([^"]*) panel')
def i_click_the_link_citation_in_the_panelname_panel(step, link, panelname):
    panel = world.firefox.find_element_by_css_selector("td.panel-container.open.%s" % panelname.lower())
    assert panel != None, "Can't find panel named %s" % panel
    
    # Click the link in the tinymc window
    anchors = panel.find_elements_by_css_selector("a.materialCitation")
    for a in anchors:
        if a.text == link:
            a.click()
    
@step(u'the ([^"]*) panel media window displays "([^"]*)"')
def the_panelname_panel_media_window_displays_title(step, panelname, title):
    panel = world.firefox.find_element_by_css_selector("td.panel-container.open.%s" % panelname.lower())
    assert panel, "Cannot find the %s panel" % panelname
    
    media_window = panel.find_element_by_css_selector('div.asset-view-published')
    try:
        a = media_window.find_element_by_css_selector('div.annotation-title a')
        assert a.text == title
    except:
        try:
            a = media_window.find_element_by_css_selector('div.annotation-title')
            assert a.text == title
        except:
            assert False, "Unable to find %s in the %s media window" % (title, panelname)
        
@step(u'I toggle the ([^"]*) panel')
def i_toggle_the_panelname_panel(step, panelname):
    pantab = world.firefox.find_element_by_css_selector("div.pantab.%s" % panelname.lower())
    assert pantab, "Cannot find the %s pantab" % panelname

    pantab.click()

    
