function rsvpscr_KCL_mac_PTB3_timeout_resp(withpulses,lang,device_resp,Path_pics, Resolution_window)
% rsvpscr_KCL_mac_PTB3(1,'french')
% use the gamepad as the response device, or keyboard otherwise  

if ~exist('withpulses','var') || isempty(withpulses), withpulses=1; end
if ~exist('lang','var') || isempty(lang), lang='french'; end
if ~exist('Path_pics','var') || isempty(Path_pics),    Path_pics=[pwd '_pic']; end
if ~exist('device_resp','var') || isempty(device_resp),    device_resp='gamepad';  end

% device_resp='gamepad'; 
% device_resp='test'; 

 max_wait_response=3;
 
 
cross_x=10;
cross_y=10;
size_line_cross=2;


%ATC: READING PICTURES PARAMETERS%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
load(fullfile(pwd,'order_pics_RSVP_SCR.mat'))
load(fullfile(pwd,'variables_RSVP_SCR.mat'))
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
offset = 5;
% ISI = [0.1 0.3 0.6];
NISI=numel(ISI);
% [~,order_ISI]=sort(rand(NISI,Nrep));
% seq_length = 10;
% times=NaN*ones(1,Nrep*(NISI+1+2+NISI*seq_length+6+1));

%ATC: INITIALIZE PARAMETERS I%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    times=NaN*ones(1,Nseq*(NISI+1+2+NISI*seq_length+6+1));
    inds_pics = zeros(1,seq_length*NISI*Nseq);
    inds_start_seq = zeros(1,Nseq);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    % tstart=0;
    times_break = [];
    cant_breaks=0;
    % answer = NaN*ones(6,Nseq);
    answer = NaN;
    deviceIndex=-1;
    dev_used=deviceIndex(end);

    if strcmp(lang,'english')
        ind_lang=1;
    elseif strcmp(lang,'spanish')
        ind_lang=2;
    elseif strcmp(lang,'french')
        ind_lang=3;
    end
    
    cl=clock;
    %ATC:print date time, etc
    prf=sprintf('-%s-%d-%d-%d-%s',date,cl(4),cl(5),round(cl(6)));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
try
    %whichScreen=0; %0=with 1 monitor, 1=laptop with external monitor
    screens=Screen('Screens');
	whichScreen=max(screens);
    
%ATC: INITIALIZE PARAMETERS II%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    
    wait_reset = 0.04;  % IT MUST BE SHORTER THAN THE SHORTEST ISI
    value_reset = 0;
%     min_cross=0.2;
    min_blank=1.25;
    max_rand_blank = 0.5;
    min_lines_onoff=0.5;
    max_rand_lines_onoff = 0.2;
%     max_rand_cross = 0.1;
%     tend_trial = 0.1;
    
%     dura_base=1.0;
    
    a=dir(sprintf('%s/*',Path_pics));
    b = zeros(length(a),1);
    b = b>0;
    for i = 1:length(a)
        b(i) = ~isempty(strfind (lower(a(i).name), '.jp'));
    end;
    a = a(b);
    if isempty(a)
        error(['No pictures for this session in ' Path_pics]);
    end
    Npic=length(a);
%     if mod(Npic,2)==1
%         error(['There is an odd number of pictures in ' Path_pics]);
%     end
    ImageNames = cell(Npic,1);
    for i=1:Npic,ImageNames{i}=a(i).name;end
        
%     ap=dir(sprintf('%s/*',Path_probes));
%     bp = zeros(length(ap),1);
%     bp = bp>0;
%     for i = 1:length(ap)
%         bp(i) = ~isempty(strfind (lower(ap(i).name), '.jp'));
%     end;
%     ap = ap(bp);
%     if isempty(ap)
%         error(['No pictures for this session in ' Path_probes]);
%     end
%     Nprobe=length(ap);
%     if Nprobe~=Nrep        
%         error(['Please be sure to have ' num2str(Nrep) ' pictures in ' Path_probes ' (half from ' Path_pics ' and the rest from somewhere else)']);
%     end
%     ProbeNames = cell(Nprobe,1);
%     for i=1:Nprobe,ProbeNames{i}=ap(i).name;end
            
    message_begin = {'Ready to begin?';'Listo para empezar?';'Etes-vous pret pour commencer?'};
%     text_endtrial = {'Press the right key to begin the next trial';'Presione la flecha derecha para continuar'};
%     text_probe = {'Have you seen this picture in the last sequence?';'Viste esta imagen en la ultima secuencia?';'Avez vous vu cette image lors de la derniere sequence?'};
    message_continue = {'Ready to continue?';'Listo para continuar?';'Etes-vous pret pour continuer?'};
    
    % session number
    cl=clock;
    prf=sprintf('-%s-%d-%d-%d',date,cl(4),cl(5),round(cl(6)));

    f=fopen(sprintf('outputs/ImageNames%s.txt',prf),'w');
    f1=fopen('outputs/ImageNames.txt','w');
    for i=1:length(a),
        fprintf(f,'%s\n',ImageNames{i});
        fprintf(f1,'%s\n',ImageNames{i});
    end
    fclose(f); fclose(f1);
    
% %     f=fopen(sprintf('ProbeNames%s.txt',prf),'w');
% %     f1=fopen('ProbeNames.txt','w');
% %     for i=1:length(ap),
% %         fprintf(f,'%s\n',ProbeNames{i});
% %         fprintf(f1,'%s\n',ProbeNames{i});
% %     end
% %     fclose(f); fclose(f1);
    

 %%%% ATC P0: DAQ configuration  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if withpulses
        %%%For using the MAC Daq toolbox%%%
        dio=DaqDeviceIndex; % get a handle for the USB-1208FS
         % configure digital port A for output
    end
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    

% WARNING !!!!this version will not work in London to sync EEG as there are
% several places with issues to maintain the odd-even sequence

%%%%%%ATC: Digital pulse signatures%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     pic_onoff = [[1 5 17];[2 8 32]];  % first pic with row 2
    pic_onoff = [[1 5 17];[3 9 33]];  % first pic with row 2
    bits_for_break = [65 128];
    lines_onoff = 77;
    blank_on = 69;
    lines_flip_blank = 103; 
    lines_flip_pic = 133; 
    trial_on = 113;
    
    
            resp_onset=79;
            resp_offset=81;
            wait_resp_on=83;
            
            
        
    %CROSSES
    cross1_on = 75;
    cross2_on = 77;
    cross2_post=91;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %     cross_on = 77;
    %     blank_on = 68;
    %     resp_on = 113;
    %     probe_on = 102; 
    
    
    data_signature_on = 85;
    data_signature_off = 84;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
 
%%%%%%ATC: Define random time parameters%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    rand('twister',sum(100*clock));
    randTime_blank = min_blank + max_rand_blank*rand(NISI+1,Nseq);  
    randTime_lines_on = min_lines_onoff + max_rand_lines_onoff*rand(1,Nseq);
    % FOR RANDOM PICTURE DURATION:
    %randTime_lines_off = randTime_blank(NISI+1,:) - (min_lines_onoff + max_rand_lines_onoff*rand(1,Nseq));
    randTime_lines_off = 1*ones(1,Nseq);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
    
    
    % Open screen.  Do this before opening the
    % offscreen windows so you can align offscreen
    % window memory to onscreen for faster copying.
    KbName('UnifyKeyNames');
%     deviceIndex=GetKeyboardIndices
    Screen('Preference','VisualDebugLevel',3);
    AssertOpenGL;    % Running on PTB-3? Abort otherwise.  

%     [window,windowRect]=Screen(whichScreen,'OpenWindow',0);
    %[window,windowRect]=Screen('OpenWindow',whichScreen,0,[0 0 1024 768]);

    [window,windowRect]=Screen('OpenWindow',whichScreen,0,Resolution_window);
    %Resolution_window=[0 0 1920 1080];
      %Resolution_window=[0 0 600 400];);
        
    %window and monitor properties
    xcenter=windowRect(3)/2;
    ycenter=windowRect(4)/2;
    
    %%ATC: define slack time (1/3 of inter-frame interval%%%%%%%%%%%%%%%
    Priority(9); %Enable realtime-scheduling in MAC
    ifi = Screen('GetFlipInterval', window, 200);
    slack=ifi/3;
    Priority(0); %Disable realtime-scheduling 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   
    
    frame_rate=1/ifi;
    white=WhiteIndex(window);
    black=BlackIndex(window);
    Screen('TextSize',window, 32); 
    
    %ATC: define structure experiment%%%%%%%%%%%%%%%%%
    experiment.pwd=pwd;
    experiment.date=date;
    experiment.xcenter=xcenter;
    experiment.ycenter=ycenter;
    experiment.frame_duration=ifi;
    experiment.frame_rate=frame_rate;
    experiment.pic=pic_onoff;
%     experiment.probe=probe_on;
%     experiment.resp=resp_on;
    experiment.blank=blank_on;    
%     experiment.cross=cross_on;
    experiment.lines_onoff=lines_onoff;
    experiment.lines_flip_blank=lines_flip_blank;
    experiment.lines_flip_pic=lines_flip_pic;
    experiment.trial_on=trial_on;
    experiment.bits_for_break=bits_for_break;
    experiment.data_signature=[data_signature_on data_signature_off];
    experiment.value_reset=value_reset;
    experiment.wait_reset=wait_reset;
    experiment.order_pic=order_pic;
%     experiment.order_probe=order_probe;
    experiment.order_ISI=order_ISI;
    experiment.ISI=ISI;
    experiment.ImageNames=ImageNames;    
    experiment.Nrep=Nrep;    
    experiment.Nseq=Nseq;    
%     experiment.isinlist=isinlist;    
    experiment.lines_change=lines_change;    
%     experiment.deviceresp=device_resp;
    
    if strcmp(device_resp,'gamepad')
        % STEP 1.5
        % Initialization of the gamepad, for collecting aswers
        numGamepads = Gamepad('GetNumGamepads');
        if (numGamepads == 0)
            error('Gamepad not connected');
        else
            [~, gamepad_name] = GetGamepadIndices;
            gamepad_index = Gamepad('GetGamepadIndicesFromNames',gamepad_name);
            gp_numButtons = Gamepad('GetNumButtons', gamepad_index);
            % gamepad button map:
            % A = 1, B = 2, X = 3, Y = 4, upper-left = 5, upper-right = 6
        end;
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
    
    
    tex=zeros(1,Npic);
    imageRect = cell(Npic,1);
    destRect = cell(Npic,1);
    for i=1:Npic,
        Im=imread(sprintf('%s/%s',Path_pics,ImageNames{i}));
        nRows=size(Im,1); nCols=size(Im,2);
        imageRect{i}=SetRect(0,0,nCols,nRows);
        destRect{i}=CenterRect(imageRect{i},windowRect);
        tex(i)=Screen('MakeTexture',window,Im);
    end

%     tex_probe=zeros(1,Nprobe);
%     imageRect_probe = cell(Nprobe,1);
%     destRect_probe = cell(Nprobe,1);
%     for i=1:Nprobe,
%         Im=imread(sprintf('%s/%s',Path_probes,ProbeNames{i}));
%         nRows=size(Im,1); nCols=size(Im,2);
%         imageRect_probe{i}=SetRect(0,0,nCols,nRows);
%         destRect_probe{i}=CenterRect(imageRect_probe{i},windowRect);
%         tex_probe(i)=Screen('MakeTexture',window,Im);
%     end
    
%     %cross
%     [Wcross, WcrossRect]=Screen('OpenOffscreenWindow',window,black);
% %     size_cross = 20;
%     size_cross = 12;
%     crect=[0 0 size_cross size_cross];
%     r1=[0 size_cross/2 size_cross size_cross/2];
%     r2=[size_cross/2 0 size_cross/2 size_cross];
%     crossRect=CenterRect(crect,WcrossRect);
%     Screen('DrawLine',Wcross,white,r1(1),r1(2),r1(3),r1(4));%,scalar*1,scalar*1);
%     Screen('DrawLine',Wcross,white,r2(1),r2(2),r2(3),r2(4));%,scalar*1,scalar*1);
    
    size_line = 5;

%     % Initialization
%     cl=clock;
%     prf=sprintf('-%s-%d-%d-%d',date,cl(4),cl(5),round(cl(6)));
%     f=fopen(sprintf('TrialOrder%s.txt',prf),'w');
%     f1=fopen('TrialOrder.txt','w');
%     for irep=1:Nrep
%         for i=1:Npic
%             fprintf(f,'%3d\n',order(i,irep));
%             fprintf(f1,'%3d\n',order(i,irep));
%         end
%     end
%     fclose(f);fclose(f1);

    HideCursor;
%%%%%ATC: MAC-KEYBOARD BASED%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%IF RUNNING IN MAC FROM A MAC MACHINE
    escapeKey = KbName('ESCAPE');
%     rightKey = KbName('RightArrow'); %writes 0 = novel %38 in Windows, 82 in MAC
%     leftKey = KbName('LeftArrow');%escribe 1 = seen %40 in Windows, 81 in MAC
%     upKey = KbName('UpArrow'); %38 in Windows, 82 in MAC
%     downKey = KbName('DownArrow'); %40 in Windows, 81 in MAC
    exitKey = KbName('x'); %88 in Windows, 27 in MAC
    spaceKey= KbName('space');  %for color changes (not really saved)
    breakKey= KbName('p');  %to pause
    
    keysOfInterest=zeros(1,256);
    scanlist=zeros(1,256);
    firstPress = zeros(1,256);
%     keysOfInterest([exitKey breakKey spaceKey])=1;
    keysOfInterest([exitKey breakKey escapeKey])=1;
    scanlist([exitKey breakKey escapeKey])=1;
    KbQueueCreate(dev_used,keysOfInterest);  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
   
    %%%%%ATC: Change to 'outputs' folder%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % save('RSVP_SCR_workspace');
    save('outputs/RSVP_SCR_workspace');
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      
%%%OLDER VERSION%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%     FlushEvents('keyDown');
%     print_message(message_begin{ind_lang},black,window);
%     %press ESC to start session
%     [~, ~, keyCode] = KbCheck(dev_used);
%     while ~keyCode(spaceKey), [~, ~, keyCode] = KbCheck(dev_used); 
%         %~keyCode(escapeKey), [~, ~, keyCode] = KbCheck(dev_used); 
%     end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
    
%%%%%ATC: Change to include GAMEPAD option%%%%%%%%%%%%%%%%%%%%%%%%%%% 
     FlushEvents('keyDown');
     print_message(message_begin{ind_lang},black,window);
        [~, ~, keyCode] = KbCheck(dev_used,scanlist);
        if strcmp(device_resp,'gamepad')
            gp_state_1 = Gamepad('GetButton', gamepad_index, 1);
            gp_state_2 = Gamepad('GetButton', gamepad_index, 2);
            while (~sum([gp_state_1, gp_state_2]))&& ~sum(keyCode([escapeKey,exitKey]))
                gp_state_1 = Gamepad('GetButton', gamepad_index, 1);
                gp_state_2 = Gamepad('GetButton', gamepad_index, 2);
                [~, ~, keyCode] = KbCheck(dev_used,scanlist);
            end;
        else
        %ATC: change key: esc per escape%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            while ~keyCode(spaceKey) %~sum(keyCode([escapeKey,exitKey]))
                [~, ~, keyCode] = KbCheck(dev_used,scanlist);
            end;
        end
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
    FlushEvents('keyDown');
    
    %%ATC enable real-time again%%%%%%%%%%%%%%%%%
    Priority(9)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    k=1;
    iind=1;
%     ka=1;    

 %%%  ATC P1: Signature paradigm onset  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if withpulses
        err_off=DaqDOut(dio,0,data_signature_on);                           %just starts
        WaitSecs(0.05);
        err_on=DaqDOut(dio,0,data_signature_off);            %pulse is on
        WaitSecs(0.45);
        err_off=DaqDOut(dio,0,data_signature_on);
        WaitSecs(0.05);
        err_on=DaqDOut(dio,0,data_signature_off);
        WaitSecs(0.45);
        err_off=DaqDOut(dio,0,data_signature_on);     
        WaitSecs(0.05);
        err_on=DaqDOut(dio,0,data_signature_off);
    end
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
  
    times(k)=GetSecs; %ATC t1
%     tprev = times(k);
    k=k+1;    
    
    KbQueueStart(dev_used);
    
%%%%%ATC: main LOOP for the sequences%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for irep=1:Nseq
        ich_blank=1;
        ich_pic=1;
        KbQueueFlush(dev_used);
        
        
        Screen('FillRect',  window,black);
        times(k)=Screen('Flip',window);%ATC t2
        
        %%% ATC P2: initial Blank screen %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if withpulses
            err=DaqDOut(dio,0,blank_on);
            WaitSecs(wait_reset);
            fff=DaqDOut(dio,0,value_reset);
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        inds_start_seq(irep)=k;
        tprev = times(k);
        k=k+1;
    
%         color_up = [255 0 0];
%         color_down = [255 0 0];
        color_up = color_start.up{irep};
        color_down = color_start.down{irep};

        Screen('FillRect',  window,black);
        %Screen('DrawLine',window,color_up,destRect{1}(1),destRect{1}(2)-offset,destRect{1}(3),destRect{1}(2)-offset,size_line);
        %Screen('DrawLine',window,color_down,destRect{1}(1),destRect{1}(4)+offset,destRect{1}(3),destRect{1}(4)+offset,size_line);   
        times(k) = Screen('Flip',window,times(k-1)+randTime_lines_on(1,irep)); %ATC t3
        
        %%%ATC P3: lines ON %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if withpulses
            err=DaqDOut(dio,0,lines_onoff);
            WaitSecs(wait_reset);
            fff=DaqDOut(dio,0,value_reset);
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%         tprev = times(k);
        k=k+1;
    
%         if lines_change{irep}{1}{ich_blank,1}==1
%             color_up = lines_change{irep}{1}{ich_blank,3};
%             color_down = lines_change{irep}{1}{ich_blank,4};
%             Screen('DrawLine',window,color_up,destRect{1}(1),destRect{1}(2)-offset,destRect{1}(3),destRect{1}(2)-offset,size_line);
%             Screen('DrawLine',window,color_down,destRect{1}(1),destRect{1}(4)+offset,destRect{1}(3),destRect{1}(4)+offset,size_line);   
%             times(k) = Screen('Flip',window,times(k-1)+lines_change{irep}{1}{ich_blank,2}); %ATC t4
%             
%             %%%ATC P4: flip blank%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%             if withpulses
%                 err=DaqDOut(dio,0,lines_flip_blank);   
%                 WaitSecs(wait_reset);
%                 fff=DaqDOut(dio,0,value_reset);
%             end
%             %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%             
%             k=k+1;
%             ich_blank = ich_blank +1;
%         end
    
        %%% randTime_blank > randTime_lines_on + lines_change{irep}{1}{ich_blank,2}
 %%%%%ATC: loop for pictures%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%       
        for iISI=1:NISI
            which_ISI = order_ISI(iISI,irep);
            order_pic
            
                            
            %%1A. CENTERED CROSS (0.5s alone)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

            Screen('DrawLine',window,white,xcenter-cross_x/2-1,ycenter,xcenter+cross_x/2+1,ycenter,size_line_cross);
            Screen('DrawLine',window,white,xcenter,ycenter-cross_y/2-1,xcenter,ycenter+cross_y/2+1,size_line_cross);
            times(k)=Screen('Flip',window,tprev+randTime_blank(iISI,irep)-slack);
            tprev = times(k);
            k=k+1;
            if withpulses
                err=DaqDOut(dio,0,cross1_on);
                WaitSecs(wait_reset);
                fff=DaqDOut(dio,0,value_reset);
            end
            
            %%%%%%%
                
            Screen('DrawTexture', window,tex(order_pic(1,which_ISI,irep)),[],destRect{order_pic(1,which_ISI,irep)},0);
            Screen('DrawLine',window,color_up,destRect{1}(1),destRect{1}(2)-offset,destRect{1}(3),destRect{1}(2)-offset,size_line);
            Screen('DrawLine',window,color_down,destRect{1}(1),destRect{1}(4)+offset,destRect{1}(3),destRect{1}(4)+offset,size_line);   
            times(k)=Screen('Flip',window,tprev+ISI(which_ISI)-slack); %ATC t5
            
            %%%ATC P5: First picture presentation%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            if withpulses
%                 err=DaqDOut(dio,0,pic_onoff(2,ceil(3*irep/Nrep)));   
                err=DaqDOut(dio,0,pic_onoff(2,ceil(3*irep/Nseq)));   
                WaitSecs(wait_reset);
                fff=DaqDOut(dio,0,value_reset);
            end
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            ipic=1 
            a(order_pic(1,which_ISI,irep),1).name
            
            inds_pics(iind)=k;
            tprev = times(k);
            k=k+1;
            iind=iind+1;
            
            if which_ISI==lines_change{irep}{2}{ich_pic,1} && lines_change{irep}{2}{ich_pic,5}==1
                Screen('DrawTexture', window,tex(order_pic(1,which_ISI,irep)),[],destRect{order_pic(1,which_ISI,irep)},0);
                color_up = lines_change{irep}{2}{ich_pic,3};
                color_down = lines_change{irep}{2}{ich_pic,4};
                Screen('DrawLine',window,color_up,destRect{1}(1),destRect{1}(2)-offset,destRect{1}(3),destRect{1}(2)-offset,size_line);
                Screen('DrawLine',window,color_down,destRect{1}(1),destRect{1}(4)+offset,destRect{1}(3),destRect{1}(4)+offset,size_line);   
                times(k) = Screen('Flip',window,tprev+lines_change{irep}{2}{ich_pic,2}-slack); %ATC t6
                
                %%%ATC P6: if line change%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                if withpulses
                    err=DaqDOut(dio,0,lines_flip_pic);   
                    WaitSecs(wait_reset);
                    fff=DaqDOut(dio,0,value_reset);
                end
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                
                k=k+1;
                ich_pic = ich_pic +1;
            end
            
                Screen('FillRect',  window,black);
                times(k) = Screen('Flip',window,tprev+randTime_lines_off(1,irep)-slack);%ATC t11

                %%%ATC P11: lines OFF%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                if withpulses
                    err=DaqDOut(dio,0,lines_onoff);
                    WaitSecs(wait_reset);
                    fff=DaqDOut(dio,0,value_reset);
                end
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %             tprev = times(k);
                k=k+1;
            
                  %%ATC 22/09/2020   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                FlushEvents('keyDown');
                    t2wait = max_wait_response; 
                    % if the wait for presses is in a loop, 
                    % then the following two commands should come before the loop starts
                    % restrict the keys for keyboard input to the keys we want
                    %RestrictKeysForKbCheck(activeKeys);
                    % suppress echo to the command line for keypresses
                    %ListenChar(2);
                    % get the time stamp at the start of waiting for key input 
                    % so we can evaluate timeout and reaction time
                    % tStart can also be the timestamp for the onset of the stimuli, 
                    % for example the VBLTimestamp returned by the 'Flip'
                    tStart = GetSecs;
                    % repeat until a valid key is pressed or we time out
                    timedout = false;
                    
%                     
%                     [~, ~, keyCode] = KbCheck(dev_used);
%                     while ~keyCode(spaceKey) && 
%                         [~, ~, keyCode] = KbCheck(dev_used); 
%                     end
%                     
                    while ~timedout,
                        % check if a key is pressed
                        % only keys specified in activeKeys are considered valid
                        
                          if strcmp(device_resp,'gamepad')
                                    gp_state_1 = Gamepad('GetButton', gamepad_index, 1);
                                    gp_state_2 = Gamepad('GetButton', gamepad_index, 2);
%                                     while (~sum([gp_state_1, gp_state_2]))&& ~sum(keyCode([escapeKey,exitKey]))
%                                         gp_state_1 = Gamepad('GetButton', gamepad_index, 1);
%                                         gp_state_2 = Gamepad('GetButton', gamepad_index, 2);
%                                         [~, keyTime, keyCode] = KbCheck(dev_used,scanlist);
%                                     end;
                                    [~, keyTime, keyCode] = KbCheck(dev_used,scanlist);
                                    if sum([gp_state_1, gp_state_2])>0
                                         if withpulses
                                            err=DaqDOut(dio,0,resp_offset);
                                            WaitSecs(wait_reset);
                                            fff=DaqDOut(dio,0,value_reset);
                                         end
                                
                                          times(k)=keyTime;
                                          %timedout = true; 
                                          tprev = times(k)
                                          k=k+1;

                                          break; 
                                    end
                                        

                          else
                             [keyIsDown, keyTime, keyCode] = KbCheck; 

%                         ~keyCode(escapeKey),
                               if keyCode(spaceKey)
                                            if withpulses
                                                err=DaqDOut(dio,0,resp_offset);
                                                WaitSecs(wait_reset);
                                                fff=DaqDOut(dio,0,value_reset);
                                            end

                                          times(k)=keyTime;
                                          %timedout = true; 
                                          tprev = times(k);
                                          k=k+1;

                                          break; 
                               end
                          end
                          
 
                          if( (keyTime - tStart) > t2wait), 
                              
                               if withpulses
                                    err=DaqDOut(dio,0,wait_resp_on);
                                    WaitSecs(wait_reset);
                                    fff=DaqDOut(dio,0,value_reset);
                                end
                              
                              times(k)=keyTime;
                              timedout = true; 
                              tprev = times(k);
                              k=k+1;
                          end
                    end
            
              %%ATC 22/09/2020   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
     
            
            
      %%%%%%%%ATC: Within sequence main pic loop ->2:seq_length%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            for ipic=2:seq_length
                ipic 
                
                %%1A. CENTERED CROSS (0.5s alone)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

                Screen('DrawLine',window,white,xcenter-cross_x/2-1,ycenter,xcenter+cross_x/2+1,ycenter,size_line_cross);
                Screen('DrawLine',window,white,xcenter,ycenter-cross_y/2-1,xcenter,ycenter+cross_y/2+1,size_line_cross);
                times(k)=Screen('Flip',window,tprev+ISI(which_ISI)-slack);
                tprev = times(k);
                k=k+1;
                if withpulses
                    err=DaqDOut(dio,0,cross1_on);
                    WaitSecs(wait_reset);
                    fff=DaqDOut(dio,0,value_reset);
                end

                                


                    
                %%%% LINES and image
                
                
                Screen('DrawTexture', window,tex(order_pic(ipic,which_ISI,irep)),[],destRect{order_pic(ipic,which_ISI,irep)},0);
                Screen('DrawLine',window,color_up,destRect{1}(1),destRect{1}(2)-offset,destRect{1}(3),destRect{1}(2)-offset,size_line);
                Screen('DrawLine',window,color_down,destRect{1}(1),destRect{1}(4)+offset,destRect{1}(3),destRect{1}(4)+offset,size_line);   
                times(k) = Screen('Flip',window,tprev+ISI(which_ISI)-slack); %ATC t7
                
                %order_pic(ipic,which_ISI,irep)
                a(order_pic(ipic,which_ISI,irep),1).name
                %%%ATC P7: Subsequent pictures (2-seq_length)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                if withpulses
%                     err=DaqDOut(dio,0,pic_onoff(mod(ipic,2)+1,ceil(3*irep/Nrep)));                     %PICTURE ONSET
                    err=DaqDOut(dio,0,pic_onoff(mod(ipic,2)+1,ceil(3*irep/Nseq)));                     %PICTURE ONSET
                    WaitSecs(wait_reset);
                    fff=DaqDOut(dio,0,value_reset);
                end
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                
                inds_pics(iind)=k;
                tprev = times(k);
                k=k+1;
                iind=iind+1;
         
                if which_ISI==lines_change{irep}{2}{ich_pic,1} && lines_change{irep}{2}{ich_pic,5}==ipic
                    Screen('DrawTexture', window,tex(order_pic(ipic,which_ISI,irep)),[],destRect{order_pic(ipic,which_ISI,irep)},0);
                    color_up = lines_change{irep}{2}{ich_pic,3};
                    color_down = lines_change{irep}{2}{ich_pic,4};
                    Screen('DrawLine',window,color_up,destRect{1}(1),destRect{1}(2)-offset,destRect{1}(3),destRect{1}(2)-offset,size_line);
                    Screen('DrawLine',window,color_down,destRect{1}(1),destRect{1}(4)+offset,destRect{1}(3),destRect{1}(4)+offset,size_line);   
                    times(k) = Screen('Flip',window,tprev+lines_change{irep}{2}{ich_pic,2}-slack);%ATC t8
                    
                    %%%ATC P8: if line change %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                    if withpulses
                        err=DaqDOut(dio,0,lines_flip_pic);   
                        WaitSecs(wait_reset);
                        fff=DaqDOut(dio,0,value_reset);
                    end
                    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                    k=k+1;
                    ich_pic = ich_pic +1;
                end
                
                Screen('FillRect',  window,black);
                times(k) = Screen('Flip',window,tprev+randTime_lines_off(1,irep)-slack);%ATC t11

                %%%ATC P11: lines OFF%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                if withpulses
                    err=DaqDOut(dio,0,lines_onoff);
                    WaitSecs(wait_reset);
                    fff=DaqDOut(dio,0,value_reset);
                end
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %             tprev = times(k);
                k=k+1;
                
                      %%ATC 22/09/2020  TIMEOUT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                     FlushEvents('keyDown');
                    t2wait = max_wait_response; 
                    % if the wait for presses is in a loop, 
                    % then the following two commands should come before the loop starts
                    % restrict the keys for keyboard input to the keys we want
                    %RestrictKeysForKbCheck(activeKeys);
                    % suppress echo to the command line for keypresses
                    %ListenChar(2);
                    % get the time stamp at the start of waiting for key input 
                    % so we can evaluate timeout and reaction time
                    % tStart can also be the timestamp for the onset of the stimuli, 
                    % for example the VBLTimestamp returned by the 'Flip'
                    tStart = GetSecs;
                    % repeat until a valid key is pressed or we time out
                    timedout = false;
                    
%                     
%                     [~, ~, keyCode] = KbCheck(dev_used);
%                     while ~keyCode(spaceKey) && 
%                         [~, ~, keyCode] = KbCheck(dev_used); 
%                     end
%                     
                    while ~timedout,
                        % check if a key is pressed
                        % only keys specified in activeKeys are considered valid
                        
                          if strcmp(device_resp,'gamepad')
                                    gp_state_1 = Gamepad('GetButton', gamepad_index, 1);
                                    gp_state_2 = Gamepad('GetButton', gamepad_index, 2);
%                                     while (~sum([gp_state_1, gp_state_2]))&& ~sum(keyCode([escapeKey,exitKey]))
%                                         gp_state_1 = Gamepad('GetButton', gamepad_index, 1);
%                                         gp_state_2 = Gamepad('GetButton', gamepad_index, 2);
%                                         [~, keyTime, keyCode] = KbCheck(dev_used,scanlist);
%                                     end;
                                    [~, keyTime, keyCode] = KbCheck(dev_used,scanlist);
                                    if sum([gp_state_1, gp_state_2])>0
                                         if withpulses
                                            err=DaqDOut(dio,0,resp_offset);
                                            WaitSecs(wait_reset);
                                            fff=DaqDOut(dio,0,value_reset);
                                         end
                                
                                          times(k)=keyTime;
                                          %timedout = true; 
                                          tprev = times(k)
                                          k=k+1;

                                          break; 
                                    end
                                        

                          else
                             [keyIsDown, keyTime, keyCode] = KbCheck; 

%                         ~keyCode(escapeKey),
                               if keyCode(spaceKey)
                                            if withpulses
                                                err=DaqDOut(dio,0,resp_offset);
                                                WaitSecs(wait_reset);
                                                fff=DaqDOut(dio,0,value_reset);
                                            end

                                          times(k)=keyTime;
                                          %timedout = true; 
                                          tprev = times(k);
                                          k=k+1;

                                          break; 
                               end
                          end
                          
 
                          if( (keyTime - tStart) > t2wait), 
                              
                               if withpulses
                                    err=DaqDOut(dio,0,wait_resp_on);
                                    WaitSecs(wait_reset);
                                    fff=DaqDOut(dio,0,value_reset);
                                end
                              
                              times(k)=keyTime;
                              timedout = true; 
                              tprev = times(k);
                              k=k+1;
                          end
                    end
            
              %%ATC 22/09/2020   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
            
            end            
            
            Screen('FillRect',  window,black);
            Screen('DrawLine',window,color_up,destRect{1}(1),destRect{1}(2)-offset,destRect{1}(3),destRect{1}(2)-offset,size_line);
            Screen('DrawLine',window,color_down,destRect{1}(1),destRect{1}(4)+offset,destRect{1}(3),destRect{1}(4)+offset,size_line);   
            times(k) = Screen('Flip',window,tprev+ISI(which_ISI)-slack); %ATC t9
            
            %%%ATC P9: blank screen%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            if withpulses
                err=DaqDOut(dio,0,blank_on);
                WaitSecs(wait_reset);
                fff=DaqDOut(dio,0,value_reset);
            end
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            tprev = times(k);
            k=k+1;

            if lines_change{irep}{1}{ich_blank,1}==1+iISI
                color_up = lines_change{irep}{1}{ich_blank,3};
                color_down = lines_change{irep}{1}{ich_blank,4};
                Screen('DrawLine',window,color_up,destRect{1}(1),destRect{1}(2)-offset,destRect{1}(3),destRect{1}(2)-offset,size_line);
                Screen('DrawLine',window,color_down,destRect{1}(1),destRect{1}(4)+offset,destRect{1}(3),destRect{1}(4)+offset,size_line);   
                times(k) = Screen('Flip',window,times(k-1)+lines_change{irep}{1}{ich_blank,2}); %ATC t10
                
                %%%ATC P10: flip lines blank%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                if withpulses
                    err=DaqDOut(dio,0,lines_flip_blank);   
                    WaitSecs(wait_reset);
                    fff=DaqDOut(dio,0,value_reset);
                end
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                
                k=k+1;
                ich_blank = ich_blank +1;
            end
            
        
        end
        
        Screen('FillRect',  window,black);
        times(k) = Screen('Flip',window,tprev+randTime_lines_off(1,irep)-slack);%ATC t11
        
        %%%ATC P11: lines OFF%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if withpulses
            err=DaqDOut(dio,0,lines_onoff);
            WaitSecs(wait_reset);
            fff=DaqDOut(dio,0,value_reset);
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%             tprev = times(k);
        k=k+1;
        
        WaitSecs(tprev+randTime_blank(NISI+1,irep)-GetSecs);
        
        % CHECK KBQUEUE (see how to collect all the spacebar presses)
        [pressed,firstPress,~,lastPress]=KbQueueCheck(dev_used);

        if pressed && firstPress(exitKey)>0
            break
        end
        
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
        
        %%%%ATC: Continue check%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        print_message(message_continue{ind_lang},black,window);
            
        Screen('FillRect',window,black);
        FlushEvents('keyDown');
        [~, ~, keyCode] = KbCheck(dev_used,scanlist);
        if strcmp(device_resp,'gamepad')
            gp_state_1 = Gamepad('GetButton', gamepad_index, 1);
            gp_state_2 = Gamepad('GetButton', gamepad_index, 2);
            while (~sum([gp_state_1, gp_state_2]))&& ~sum(keyCode([escapeKey,exitKey]))
                gp_state_1 = Gamepad('GetButton', gamepad_index, 1);
                gp_state_2 = Gamepad('GetButton', gamepad_index, 2);
                [~, ~, keyCode] = KbCheck(dev_used,scanlist);
            end;
        else
        %ATC: change key: space per escape%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            while ~keyCode(spaceKey) %~sum(keyCode([escapeKey,exitKey]))
                [~, ~, keyCode] = KbCheck(dev_used,scanlist);
            end;
        end
        times(k)=GetSecs; %ATC t12
        
        %%%ATC P12: change trial/repetition %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if withpulses
            err=DaqDOut(dio,0,trial_on);
            WaitSecs(wait_reset);
            fff=DaqDOut(dio,0,value_reset);
        end
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        k=k+1;
     %ATC: change key: esc per escape%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %if keyCode(exitKey), break; end
         if keyCode(spaceKey), break; end       
    end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       
    times(isnan(times))=[];
    inds_pics(inds_pics==0)=[];
    inds_start_seq(inds_start_seq==0)=[];
    ShowCursor;
    KbQueueStop(dev_used);
    KbQueueRelease(dev_used);    
    Screen('CloseAll');
    Priority(0); 
%     save(['timesanswer' prf], 'times', 'times_break','answer');
%     save('timesanswer','times', 'times_break','answer');

  %%%%ATC:VITAL%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %times, times_break, answer......

%     
    %%ATC:save in 'outputs'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    save(['outputs/timesanswer' prf], 'times', 'times_break','answer');
    save('outputs/timesanswer','times', 'times_break','answer');
    
    %%ATC: complete 'experiment' %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    experiment.times=times;
    experiment.inds_pics=inds_pics;
    experiment.inds_start_seq=inds_start_seq;
    experiment.answer=answer;
%     experiment.tstart=tstart;
    experiment.times_break=times_break;
    experiment.cant_breaks=cant_breaks;
%     save('RSVP_SCR_workspace');
%     save('experiment_properties','experiment');

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

   %%ATC:save in 'outputs'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    save('outputs/RSVP_SCR_workspace');
    save('outputs/experiment_properties','experiment');
   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

catch ME
    times(isnan(times))=[];
    inds_pics(inds_pics==0)=[];
    inds_start_seq(inds_start_seq==0)=[];
    try         
        [pressed,firstPress,~,lastPress]=KbQueueCheck(dev_used);
        KbQueueStop(dev_used);
        KbQueueRelease(dev_used);
    catch
        disp('did not create the keyboard queue')
    end
    Screen('CloseAll')
    Priority(0);
%     save(['timesanswer' prf], 'times', 'times_break','answer');
%     save('timesanswer','times', 'times_break','answer');

    %%ATC:save in 'outputs'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    save(['outputs/timesanswer' prf], 'times', 'times_break','answer');
    %save('outputs/timesanswer','times', 'times_break','answer');
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    experiment.times=times;
    experiment.inds_pics=inds_pics;
    experiment.inds_start_seq=inds_start_seq;
    experiment.answer=answer;
%     experiment.tstart=tstart;
    experiment.times_break=times_break;
    experiment.cant_breaks=cant_breaks;
    experiment.ME=ME;
%     save('RSVP_SCR_workspace');
%     save('experiment_properties','experiment');

   %%ATC:save in 'outputs'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    save('outputs/RSVP_SCR_workspace');
    save('outputs/experiment_properties','experiment');
   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   
    ShowCursor;
    rethrow(ME)
end

function print_message(message,black,window)
Screen('FillRect',  window,black);
DrawFormattedText(window, message, 'center', 'center', [255 255 255]);
Screen('Flip',window);