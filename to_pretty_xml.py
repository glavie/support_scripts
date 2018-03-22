import sys

from xml.dom.minidom import parse

args = sys.argv

file = parse(args[1])

file = file.toprettyxml(encoding='UTF-8')

pretty_xml = open(args[2], 'w')

pretty_xml.write(file)

pretty_xml.close()

