import os
from lxml import etree
from copy import deepcopy
from math import floor


def split_iati(target_mb, filename, out_dir=None):
    # Parse XML
    if out_dir is None:
        out_dir = os.path.dirname(filename)
    print("Output will be saved in {}.".format(out_dir))
    filename_base = os.path.splitext(os.path.basename(filename))[0]
    tree = etree.parse(filename)
    root = tree.getroot()

    # Get root activities
    root_activities = root.xpath("//iati-activity")

    # Calculate rough activities per file
    length_activities = len(root_activities)
    filesize_mb = os.stat(filename).st_size / (1024 * 1024)
    target_ratio = min(target_mb / filesize_mb, 1)
    max_activities = round(length_activities * target_ratio)

    # Copy iati-activities element so we can repeat it verbatim
    base = etree.Element("iati-activities", **root.attrib)

    # Incrementally copy activities into blank bases
    base_copy = deepcopy(base)
    for i in range(0, len(root_activities)):
        root_activity = deepcopy(root_activities[i])
        base_copy.append(root_activity)
        if i % max_activities == max_activities - 1 or i == len(root_activities) - 1:  # Write once for every max_activities or once we reach the end
            doc = etree.ElementTree(base_copy)
            file_counter = floor(i / max_activities)
            out_filename = "{}-{}.xml".format(filename_base, file_counter)
            print("Writing {}...".format(out_filename))
            with open(os.path.join(out_dir, out_filename), "wb") as xmlfile:
                doc.write(xmlfile, encoding="utf-8", pretty_print=True)
            base_copy = deepcopy(base)

    print("Done.")


if __name__ == "__main__":
    split_iati(
        1,
        "/home/alex/git/iati-splitter/Japan/Japan-Technical-Cooperation-Activities.xml",
        "/home/alex/git/iati-splitter/Japan/Japan-split"
    )
