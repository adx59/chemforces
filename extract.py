#!/usr/bin/env python3
import pdf2image
import PIL
import os
import pytesseract

input_f = "pdfs/2013.pdf"

# stolen from stack
def trim(im):
    bg = PIL.Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = PIL.ImageChops.difference(im, bg)
    diff = PIL.ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

# stolen from stack
def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = PIL.Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def segment_problems(side_image, year, page, firstprobnum, lastseg=False):
    """Segment a left/right side of USNCO open into its problems
    
    Returns the last problem NOT segmented on a page (n+1)"""
    current_prob = firstprobnum

    imdex = side_image.crop((0, 0, 30, side_image.height))
    p_locs = []

    # preliminary # detection
    # really messy algo
    for block in range(0, int(side_image.height/30)):
        content = False
        for x in range(0, 30):
            for y in range(block*30, block*30+30):
                if imdex.getpixel((x, y)) != (255, 255, 255):
                    p_locs.append(block*30)
                    content = True
                    break
            if content:
                break

    # finish detecting problem bounds
    locs = []
    for loc in range(len(p_locs)):
        if p_locs[loc] == p_locs[loc-1] + 30:
            continue
        locs.append(p_locs[loc])

        imdex.putpixel((0, p_locs[loc]), (0, 0, 255))
    
    # segment problems out & save
    for problem in range(1, len(locs)):
        imp = side_image.crop((0, locs[problem-1], side_image.width, locs[problem]))
        imp = trim(imp)
        imp = add_margin(imp, 20, 20, 20, 20, (255, 255, 255))

        imp.save(f"{year}/probs/{current_prob}.png")
        current_prob += 1

    imp = side_image.crop((0, locs[-1], side_image.width, side_image.height))
    imp = trim(imp)
    imp = add_margin(imp, 20, 20, 20, 20, (255, 255, 255))
    
    imp.save(f"{year}/probs/{current_prob}.png")
    current_prob += 1

    return current_prob

FIRST_PAGE_CROP = 320 # 280 by default
LAST_PAGE_CROP = 65 # 65 by default

def segment(image, year, page, firstprobnum, lastpage=False):
    """Segment a page of a USNCO open into its problems
    
    Returns the last problem NOT segmented on a page (n+1)"""
    pn = firstprobnum
    failure = [False, False]

    # initial crop
    im = image.crop((0, 120, image.width, image.height-200))  
    if page == 2:
        im = im.crop((0, FIRST_PAGE_CROP, im.width, im.height))

    # left-right sep
    iml = im.crop((0, 0, im.width/2, im.height))
    imr = im.crop((im.width/2, 0, im.width, im.height))
    iml = trim(iml)
    imr = trim(imr)

    # check if right or left does not have content
    try:
        pytesseract.image_to_string(iml)
    except:
        # no text
        print(f"{year}, {page} left seg failed")
        failure[0] = True

    try:
        pytesseract.image_to_string(imr)
    except:
        # no text
        print(f"{year}, {page} right seg failed")
        failure[1] = True

    if lastpage:
        print("Segmenting last page")
        if failure[1]:
            iml = iml.crop((0, 0, iml.width, iml.height-LAST_PAGE_CROP))
            iml = trim(iml)
        else:
            imr = imr.crop((0, 0, imr.width, imr.height-LAST_PAGE_CROP))
            imr = trim(imr)

    if not failure[0]:
        start = pn
        pn = segment_problems(iml, year, page, start)

        iml.save(f"{year}/halves/{start}_{pn-1}.png")
        print(f"Segmented problems {start} - {pn-1}. Check {year}/halves/{start}_{pn-1}.png")

    if not failure[1]:
        start = pn
        pn = segment_problems(imr, year, page, start)

        imr.save(f"{year}/halves/{start}_{pn-1}.png")
        print(f"Segmented problems {start} - {pn-1}. Check {year}/halves/{start}_{pn-1}.png")

    return pn

LAST_PAGE_PADDING = 2 # 1 by default
        
def exam_to_img(inp):
    pgs = pdf2image.convert_from_path(inp)
    year = os.path.basename(open(inp).name).split(".")[0]

    if not os.path.exists(f"{year}"):
        os.makedirs(f"{year}")
        os.makedirs(f"{year}/pages")
        os.makedirs(f"{year}/halves")
        os.makedirs(f"{year}/probs")

    pn = 1
    for i in range(2, len(pgs)-LAST_PAGE_PADDING):
        start = pn
        pn = segment(pgs[i], year, i, pn, i == len(pgs)-LAST_PAGE_PADDING-1)

        pgs[i].save(f"{year}/pages/{start}_{pn-LAST_PAGE_PADDING}.png")

        # debugging: only attempt to seg first page
        # break

if __name__ == "__main__":
    for year in range(2011, 2012):
        print(f"Segmenting pdfs/{year}.pdf")
        exam_to_img(f"pdfs/{year}.pdf")
