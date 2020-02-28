import os
from lxml import etree
from copy import deepcopy
from math import floor


def get_identifier(activity):
    return activity.xpath("//iati-identifier")[0].text


def split_iati(max_activities, filename):
    # Parse XML
    filename_base = os.path.splitext(filename)[0]
    tree = etree.parse(filename)
    root = tree.getroot()

    # Sort root activities
    root_activities = root.xpath("//iati-activity")
    root_activities[:] = sorted(root_activities, key=get_identifier)

    # Copy iati-activities element so we can repeat it verbatim
    base = deepcopy(root)
    for base_activity in base.getchildren():
        base.remove(base_activity)

    # Incrementally copy activities into blank bases
    base_copy = deepcopy(base)
    for i in range(0, len(root_activities)):
        root_activity = deepcopy(root_activities[i])
        base_copy.append(root_activity)
        if i % max_activities == max_activities - 1:  # Write once for every max_activities
            doc = etree.ElementTree(base_copy)
            file_counter = floor(i / max_activities)
            with open("{}-{}.xml".format(filename_base, file_counter), "wb") as xmlfile:
                doc.write(xmlfile, encoding="utf-8", pretty_print=True)
            base_copy = deepcopy(base)
        elif i == len(root_activities) - 1:  # Or once we reach the end
            doc = etree.ElementTree(base_copy)
            file_counter = floor(i / max_activities)
            with open("{}-{}.xml".format(filename_base, file_counter), "wb") as xmlfile:
                doc.write(xmlfile, encoding="utf-8", pretty_print=True)
            base_copy = deepcopy(base)


if __name__ == "__main__":
    max_activities = 10
    filename = "/home/alex/git/iati-splitter/test.xml"
    split_iati(max_activities, filename)
