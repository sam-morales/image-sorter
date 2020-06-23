import os, time, datetime, shutil
from os import scandir
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

def Walk(basedir):
    '''
    Recursively yield DirEntry objects for given directory
    '''
    for entry in scandir(basedir):
        if entry.is_dir(follow_symlinks=False):
            station = DetermineInspection(entry.path, stations)
            if station is not None:
                print(f"Checking folder for {station}")
                check_station = selected.get(station)
                if check_station is not None and check_station.get():
                    if get_fail.get() and "FAIL" in entry.path:
                        yield from Walk(entry.path)
                    if get_pass.get() and "PASS" in entry.path:
                        yield from Walk(entry.path)
                    else:
                        print(f"Not checking {entry.path} since PASS image retrieval not set")
            else:
                yield from Walk(entry.path)
        else:
            yield entry.path

def SortImages(sort_states, date):
    sort_directory = filedialog.askdirectory(title="Source Directory")
    destination_directory = filedialog.askdirectory(title="Destination Directory")
    sort_date = date.get()
    counter = 0
    
    print(f"Directory to Sort: {sort_directory}")
    print(f"Destination Directory: {destination_directory}")
    print(f"Sort Date: {sort_date}")

    for img in Walk(sort_directory):
        print(img)
        modtime_epoch = os.path.getmtime(img)
        modified_time = datetime.datetime.fromtimestamp(modtime_epoch).strftime('%Y-%m-%d')
        print(f"Found image was modified: {modified_time}")

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

            check_station = selected.get(station)
            try: 
                print(f"Station {station} is set to {check_station.get()}")
            except:
                print("No station detected in image filename")
            
            # Determine if the determined station is one we are looking for
            if check_station is not None and check_station.get():
                #Copy the file only if it is a fail
                if("FAIL" in imagename.upper()):
                    destination_path = dated_folder + '/' + station + '/' + imagename

                    print(f"Image from station {station}")
                    print(f"Copying image {imagename} to {destination_path}")
                
                    shutil.copy2(img, destination_path)
                    counter += 1

    print(f"Moved {counter} images. Image copying complete!")

# Station names for system
stations = [ 'C10S60', 'C15S60', 'C30S30', 'C30S60', 'C60S35', 'C60S60', 'C80S22', 'C80S50', 'C80S65' , 'C80S70', 'C80S75']
selected = {}

# UI creation and setup
y = 0
x = 0
root = Tk()
get_pass = BooleanVar()
get_fail = BooleanVar()
root.title("Kateri Image Sorter V3.2")

for station in stations:
    if x not in range(0, 3):
        y += 1
        x = 0
       
    is_selected = BooleanVar()
    box = Checkbutton(root, text=station, variable=is_selected, \
          onvalue=True, offvalue=False, height=3, width=20 )
    selected[station] = is_selected
    box.grid(row=y, column=x)
    x += 1

# Button creation
pass_button = Checkbutton(root, text="Get Pass", variable=get_pass,
                            onvalue=True, offvalue=False, height=3, width=20)
fail_button = Checkbutton(root, text="Get Fail", variable=get_fail,
                            onvalue=True, offvalue=False, height=3, width=20)
entry = Entry(root)
entry.insert(0, "yyyy-mm-dd")
go_button = Button(root, text="GO", fg="green", command=lambda : SortImages(selected, entry))

# Button grid alignment
entry.grid(row=y+2, column=0)
pass_button.grid(row=y+2, column=1)
fail_button.grid(row=y+2, column=2)
go_button.grid(row=y+3, column=2)

fail_button.toggle()

root.mainloop()
