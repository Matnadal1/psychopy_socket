
clear all
clear all
clear all

dio=DaqDeviceIndex; % get a handle for the USB-1208FS
hwline=DaqDConfigPort(dio,0,0); % configure digital port A for output

values = [1 2 5 8 17 32 65 128 85 84 4 16 0];
%%
for i=1:length(values)
    err=DaqDOut(dio,0,values(i));
    pause(0.4)
end