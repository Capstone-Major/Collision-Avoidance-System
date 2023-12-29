# def decideRegion(x1,x2,points):
#     def check_region(x, points):
#         # Check which region the point belongs to
#         for i, point in enumerate(points[:-1]):
#             if x >= point and x <= points[i + 1]:
#                 return (i+1)

#         # Check if the point is in the last region
#         if x >= points[-1]:
#             return f"Region {len(points)}"

#         return "Outside of any region"

#     def find_intersected_regions(x1, x2, points):
#         intersected_regions = []

#         # Check for regions intersected by x1
#         region_x1 = check_region(x1, points)
#         if region_x1 not in intersected_regions:
#             intersected_regions.append(region_x1)

#         # Check for regions intersected by x2
#         region_x2 = check_region(x2, points)
#         if region_x2 not in intersected_regions:
#             intersected_regions.append(region_x2)

#         return intersected_regions

#     # Find intersected regions
#     intersected_regions = find_intersected_regions(x1, x2, points)

#     regionList =[]
#     # Print the result
#     if intersected_regions:
#         # print("Line intersects with the following regions:")
#         for region in intersected_regions:
#             regionList.append(region)
#     else:
#         print("Line does not intersect with any region.")

#     return regionList

# # print(decideRegion(1,29,[0, 10, 20, 30, 40]))

def decideRegion(boxes, points, width):
    regions = set()  # .add(x)

    for i in boxes:
        maxi = -5
        mini = 5
        if abs(i[0]-i[1]) <= width/4:
            if (i[0] < width/4) or (i[1] < width/4):
                regions.add(1)
            if (i[0] >= width/4 and i[0] <= width/2) or (i[1] >= width/4 and i[1] <= width/2):
                regions.add(2)
            if ((i[0] >= width/2 and i[0] <= (3*width)/4)) or ((i[1] >= width/2 and i[1] <= (3*width)/4)):
                regions.add(3)
            if ((i[0] >= (3*width)/4) and i[0] <= width) or ((i[1] >= (3*width)/4) and i[1] <= width):
                regions.add(4)

        else:

            if (i[0] < width/4) or (i[1] < width/4):
                # regions.add(2)
                maxi = max(maxi, 1)
                mini = min(mini, 1)
            if (i[0] >= width/4 and i[0] <= width/2) or (i[1] >= width/4 and i[1] <= width/2):
                # regions.add(2)
                maxi = max(maxi, 2)
                mini = min(mini, 2)
            if ((i[0] >= width/2 and i[0] <= (3*width)/4)) or ((i[1] >= width/2 and i[1] <= (3*width)/4)):
                # regions.add(3)
                maxi = max(maxi, 3)
                mini = min(mini, 3)
            if ((i[0] >= (3*width)/4) and i[0] <= width) or ((i[1] >= (3*width)/4) and i[1] <= width):
                # regions.add(3)
                maxi = max(maxi, 4)
                mini = min(mini, 4)

        for j in range(mini, maxi+1):
            regions.add(j)
        print('range:-', mini, maxi)
    return list(regions)
