
#########################################################################################################

# Romain SAVIDAN

#########################################################################################################
# imports
import math

# global variables
Xsize, Ysize = 800, 800 # window size
places = []
minX, maxX = 0, 0 # min/max long of cities
minY, maxY = 0, 0 # min/max lat of cities
minDensity, maxDensity = 0.0, 0.0
minPopulation, maxPopulation = 0, 0
minPopulationSize = 50000  # minimum population for a circle to be displayed
labelFontPath = '/home/roms/Desktop/Dropbox/Telecom/TP/Visualization/TP1_pyde/data/Ubuntu-32.vlw'
black = color(0) # color for fonts
red = color(196, 0, 0)
backgroundCol = 255
minPopulationToDisplay = 100
valuePressed = ''

# color and shape values (cities color will be from clear to dark)
clearValueR = 140
darkValueR = 46
clearValueG = 140
darkValueG = 0
clearValueB = 140
darkValueB = 46
ellipseColor = color(5,0,5,int(0.75*255))
clearValueR2 = 227
darkValueR2 = 196
clearValueG2 = 133
darkValueG2 = 0
clearValueB2 = 133
darkValueB2 = 0


# radius of ellipse for cities
minRadius = 1
maxRadius = 50

# city that has been cliked on
lastPlacePicked = None
placesPicked = []

# zoom parameters
zoom = 1.0
zoomStep = 0.25
Xoffset = 0
Yoffset = 80
offsetStep = 0.25 * min(Xsize, Ysize) / zoom
zoomBoxX = 25
zoomBoxY = 100

#########################################################################################################
# main processing functions

def setup():
    ellipseMode(RADIUS)
    colorMode(RGB)
    size(Xsize, Ysize)
    readData()
    # all drawing will use black labelFont at 32 point.
    labelFont = loadFont(labelFontPath)    
    textFont(labelFont, 20)

def draw():
    scale(zoom) # zoom level
    background(backgroundCol) # clears the screen
    # draws map of France
    countPop = 0
    countPlaces = 0
    for place in places:
        # draws cities with pop > min
        if (place.population >= minPopulationToDisplay):
            place.draw()
            countPop += place.population
            countPlaces += 1
    # add the population displayed and number of cities
    noStroke()
    fill(255, 255, 255, 255*0.95)
    rect(0, 0, Xsize, 60 / zoom)
    textSize(20 / zoom)
    fill(black)
    text('Displaying populations above ' + str(minPopulationToDisplay) + ' (' + str(countPop) + ' people in ' + str(countPlaces) + ' cities)', 35 / zoom, 35 / zoom)
    # displays the picked up cities
    fill(red)
    for place in placesPicked:
        u = len(place.name)
        x = place.x
        y = place.y - place.radius - 5
        textAlign(CENTER)
        text(place.name + ' (' + str(place.postalCode) + ')', x, y)
    textAlign(BASELINE)

#########################################################################################################
# load data

def readData():
    global minX, maxX, minY, maxY, minDensity, maxDensity, minPopulation, maxPopulation
    #lines = loadStrings("http://www.infres.enst.fr/~eagan/class/as2014/inf229/data/population.tsv")
    lines = loadStrings(
        "/home/roms/Desktop/Dropbox/Telecom/TP/Visualization/population.tsv")
    # First line contains metadata
    # Second line contains column labels
    # Third line and onward contains data cases
    for line in lines[2:]:
        columns = line.split("\t")
        place = Place()
        place.postalCode = int(columns[0])
        place.longitude = float(columns[1])
        place.latitude = float(columns[2])
        place.name = columns[4]
        place.population = int(columns[5])
        place.density = float(columns[6])
        places.append(place)
    minX = min(places, key=lambda place: place.longitude).longitude
    maxX = max(places, key=lambda place: place.longitude).longitude
    minY = min(places, key=lambda place: place.latitude).latitude
    maxY = max(places, key=lambda place: place.latitude).latitude
    minDensity = min(places, key=lambda place: place.density).density
    maxDensity = max(places, key=lambda place: place.density).density
    minPopulation = min(places, key=lambda place: place.population).population
    maxPopulation = max(places, key=lambda place: place.population).population
    # sort places by population
    places.sort(key = lambda place : place.population, reverse = True)

#########################################################################################################
# user interactions

def keyPressed():
    # changes the minPopulationToDisplay threshold
    global valuePressed, minPopulationToDisplay, zoom, zoomStep, Xoffset, Yoffset, offsetStep, zoomBoxX, zoomBoxY, placesPicked
    digits = ['0','1','2','3','4','5','6','7','8','9']
    # adds digits to pressed strings
    if (key in digits):
        valuePressed = valuePressed + str(key)
        #print valuePressed
    # if enter is pressed, change the threshold
    if (valuePressed != '' and key == ENTER):
        minPopulationToDisplay = int(valuePressed)
        redraw()
        valuePressed = ''
    # zoom + and -
    if(key == '-' and zoom > zoomStep):
        noStroke()
        fill(255, 255, 255, 255 * 0.90)
        rect(zoomBoxX / zoom, zoomBoxY / zoom, 150 / zoom, 50 / zoom)
        textSize(16 / zoom)
        fill(0, 0, 0)
        text('Zooming: ' + str(zoom - zoomStep) + 'x', (zoomBoxX + 15) / zoom, (zoomBoxY + 30) / zoom)
        zoom -= zoomStep
        offsetStep = 0.25 * min(Xsize, Ysize) / zoom
    if(key == '+' and zoom < 1.0 + 12 * zoomStep):
        noStroke()
        fill(255, 255, 255, 255 * 0.90)
        rect(zoomBoxX / zoom, zoomBoxY / zoom, 150 / zoom, 50 / zoom)
        textSize(16 / zoom)
        fill(0, 0, 0)
        text('Zooming: ' + str(zoom + zoomStep) + 'x', (zoomBoxX + 15) / zoom, (zoomBoxY + 30) / zoom)
        zoom += zoomStep
        offsetStep = 0.25 * min(Xsize, Ysize) / zoom
    # goes right, left, up, down
    if(keyCode == LEFT):
        Xoffset += offsetStep
    if(keyCode == RIGHT):
        Xoffset -= offsetStep
    if(keyCode == UP):
        Yoffset += offsetStep
    if(keyCode == DOWN):
        Yoffset -= offsetStep
    # cancel all changes
    if(key == 'z'):
        zoom = 1.0
        Xoffset = 0
        Yoffset = 80
        offsetStep = 0.25 * min(Xsize, Ysize) / zoom
    if(key == 'r'):
        for place in placesPicked:
            place.highlighted = False
        placesPicked = []
        #redraw()


def mousePressed():
    global lastPlacePicked, zoom
    xPressed = mouseX / zoom #(mouseX + Xoffset) / zoom
    yPressed = mouseY / zoom #(mouseY + Yoffset) / zoom
    picked = pick(xPressed, yPressed)
    if(picked in placesPicked):
        picked.highlightOnOff()
        placesPicked.remove(picked)
    elif(picked not in placesPicked and picked != None):
        picked.highlightOnOff()
        placesPicked.append(picked)    


def pick(x, y):
    picked = None
    for place in reversed(places):
        if(place.contains(x, y)):
            picked = place #.name + ' (' + str(place.postalCode) + ')'
            break
    return picked

#########################################################################################################
# class for cities

class Place(object):
    #minX, maxX = (0, 0)
    #minY, maxY = (0, 0)
    longitude = 0
    latitude = 0
    name = ""
    postalCode = 0
    population = -1
    density = -1
    highlighted = False

    @property
    def x(self):
        return map(self.longitude, minX, maxX, 0 + Xoffset, width + Xoffset)

    @property
    def y(self):
        return map(self.latitude, minY, maxY, height + Yoffset, 0 + Yoffset)

    @property
    def color_(self):
        # picks up color
        if(self.density > 0):
            densityPercent = (math.log(self.density,10)) / (math.log(maxDensity,10))
        else:
            densityPercent = 0
        # transparency is different depending on whether it is highligthed or not
        if(self.highlighted == True):
            colValueR = int(clearValueR2 + densityPercent * (darkValueR2 - clearValueR2))
            colValueG = int(clearValueG2 + densityPercent * (darkValueG2 - clearValueG2))
            colValueB = int(clearValueB2 + densityPercent * (darkValueB2 - clearValueB2))
            transparency = int(.50*255)
        else:
            colValueR = int(clearValueR + densityPercent * (darkValueR - clearValueR))
            colValueG = int(clearValueG + densityPercent * (darkValueG - clearValueG))
            colValueB = int(clearValueB + densityPercent * (darkValueB - clearValueB))
            transparency = int(.50*255)
        return color(colValueR, colValueG, colValueB, transparency)

    @property
    def radius(self):
        return max(minRadius, int(maxRadius * math.sqrt(self.population / float(maxPopulation))))

    def contains(self, x, y):
        response = False
        if(x >= self.x - self.radius and x <= self.x + self.radius and y >= self.y - self.radius and y <= self.y + self.radius):
            response = True
        return response

    def highlightOnOff(self):
        self.highlighted = not(self.highlighted)

    def draw(self):
        try:
            # draws point(x,y) with color corresponding to density
            #set(self.x, self.y, self.color_)
            # draw ellipse
            fill(self.color_)
            noStroke()
            ellipse(self.x, self.y, self.radius, self.radius)
        except:
            pass

