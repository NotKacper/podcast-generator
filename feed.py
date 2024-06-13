import yaml
import xml.etree.ElementTree as xml_tree

with open("feed.yaml",'r') as file:
    yaml_data = yaml.safe_load(file) #loads the .yaml file, ensuring it loads correctly.

rss_element = xml_tree.Element('rss', { # this creates an rss element - an element is a tag in the XML language (like an element in HTML)
'version':'2.0',
'xmlns:itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd',
'xmlns:content':'http://purl.org/rss/1.0/modules/content/'})

channel_element = xml_tree.SubElement(rss_element, 'channel') # creates a channel tag inside of the main rss element

link_prefix = yaml_data['link']

xml_tree.SubElement(channel_element, 'title').text = yaml_data['title'] # creates a title sub element inside the channel element.
xml_tree.SubElement(channel_element, 'format').text = yaml_data['format'] # creates a format sub element inside the channel element.
xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle'] # creates a subtitle sub element inside the channel element.
xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author'] # creates a author sub element inside the channel element.
xml_tree.SubElement(channel_element, 'itunes:image', {'href':link_prefix + yaml_data['image']}) # creates a image sub element inside the channel element.
xml_tree.SubElement(channel_element, 'language').text = yaml_data['language'] # creates a language sub element inside the channel element.
xml_tree.SubElement(channel_element, 'link').text = link_prefix # creates a link sub element inside the channel element.

xml_tree.SubElement(channel_element, 'itunes:category', {'text':yaml_data['category']}) # creates a link sub element inside the channel element.

#reads every entry from the item category in the yaml file.
for item in yaml_data['item']:
    item_element = xml_tree.SubElement(channel_element, 'item')
    xml_tree.SubElement(item_element, 'title').text = item['title']
    xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data['author']
    xml_tree.SubElement(item_element, 'description').text = item['description']
    xml_tree.SubElement(item_element, 'itnues:duration').text = item['duration']
    xml_tree.SubElement(item_element, 'pubDate').text = item['published']

    enclosure = xml_tree.SubElement(item_element, 'enclosure', {
        'url': link_prefix + item['file'],
        'type': 'audio/mpeg',
        'length': item['length']
    })

output_tree = xml_tree.ElementTree(rss_element) # creates an XML tree representing the XML file.

output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True) # writes the XML tree to an XML file called podcast.xml
