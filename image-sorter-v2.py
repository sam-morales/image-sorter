import glob, os, time, datetime, shutil
from tkinter import filedialog
from tkinter import *

def CreateDirectories (base_path, stations):
    '''
    Creates the base folder tree for the date and the subsequent stations
    '''
    os.mkdir(base_path)
    for station in stations:
        os.mkdir(base_path + '/' + station + '/')

def DetermineInspection (filename, stations):
    for s in stations:
        if s in filename: return s

def SortImages(sort_states):
    sort_directory = "C:/Users/samue/Downloads/Images" #filedialog.askdirectory(title="Source Directory")
    destination_directory = "C:/Users/samue/OneDrive/Pictures/Test" #filedialog.askdirectory(title="Destination Directory")

    sort_date = '2020-04-15' #input("Enter the date for retrieval (Format yyyy-mm-dd): ")

    print(f"Directory to Sort: {sort_directory}")
    print(f"Destination Directory: {destination_directory}")
    print(f"Sort Date: {sort_date}")

    images = glob.glob(sort_directory + '/**/*.png', recursive=True)

    for img in images:
        modtime_epoch = os.path.getmtime(img)
        modified_time = datetime.datetime.fromtimestamp(modtime_epoch).strftime('%Y-%m-%d')

        #Check if the file's modified date matches the required sort date
        if sort_date == modified_time:
            dated_folder = destination_directory + '/' + sort_date

            #Create the path if it does not exist
            if not os.path.isdir(dated_folder):
                CreateDirectories(dated_folder, stations)

            # Determine station and image names    
            station = DetermineInspection(img, stations)
            imagename = os.path.basename(img)
            print(f"Image name is: {imagename}")
            '''
            print(f"Available stations are: {stations}")
            print(f"Station is: {station}")
            for s, value in selected.items():
                print(f"Station {s} is {value.get()}")
            '''
            check_station = selected.get(station)
            try: 
                print(f"Station {station} is set to {check_station.get()}")
            except:
                print("No station detected in image filename")
            
            # Determine if the determined station is one we are looking for
            if check_station is not None and check_station.get():
                #Copy the file only if it is a fail
                if(imagename.find("FAIL")):
                    destination_path = dated_folder + '/' + station + '/' + imagename

                    print(f"Image from station {station}")
                    print(f"Copying image {imagename} to {destination_path}")
                
                    shutil.copy2(img, destination_path)

root = Tk()

# Station names for system
#stations = { 'C15S60' : chkC15S60, 'C30S30' : chkC30S30, 'C30S60' : chkC30S60, 'C60S35' : chkC60S35, 'C60S60' : chkC60S60, 'C80S22' : chkC80S22, 'C80S50' : chkC80S50, 'C80S65' : chkC80S65 }
stations = [ 'C15S60', 'C30S30', 'C30S60', 'C60S35', 'C60S60', 'C80S22', 'C80S50', 'C80S65' ]
selected = {}
# UI creation and setup
for station in stations:
    is_selected = BooleanVar()
    box = Checkbutton(root, text=station, variable=is_selected, \
        onvalue=True, offvalue=False, height=3, width=40 )
    selected[station] = is_selected
    box.pack()

button1 = Button(root, text="QUIT", fg="red", command=quit)
button1.pack()
button2 = Button(root, text="Okay", command=lambda: SortImages(stations))
button2.pack()

root.mainloop()