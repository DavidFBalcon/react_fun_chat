import validators

def check_images(to_check, imgArray):
    extensions = [".jpg", ".png", ".gif"]
    has_image = False
    for i in range(len(to_check)):
        if validators.url(to_check[i]):
            has_image = True
            if(to_check[i][-4:] in extensions):
                imgArray.append(to_check[i])
            to_check[i] = "<a href=" + "\"" + to_check[i] + "\">" + to_check[i] + "</a>"
    return has_image