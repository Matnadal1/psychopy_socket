                     
                                                     
     clc   %tic
    %Resolution_window=[0 0 1280 800];  
    %Resolution_window=[0 0 1920 1080];
    %Resolution_window=[0  0 600 400];
      
    
     
    
    Resolution_window=[0 0 1024 768];
    %Resolution_window=[0 0 1280 800];
      
    withpulses=0;
    lang='spanish';
    %device_resp='keyboard';        
    device_resp='gamepad';
    Path_pics=[];     
        
    %tic  
    %rsvpscr_KCL_mac_PTB3(withpulses,lang,device_resp,Path_pics,Resolution_window)
    rsvpscr_KCL_mac_PTB3_timeout_resp(withpulses,lang,device_resp,Path_pics,Resolution_window)  
    %toc                                                                                               