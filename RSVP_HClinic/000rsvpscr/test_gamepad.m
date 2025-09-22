clear all
clear all
clear all
clc

KbName('UnifyKeyNames');
exitKey = KbName('x'); %88 in Windows, 27 in MAC


numGamepads = Gamepad('GetNumGamepads');
if (numGamepads == 0)
    error('Gamepad not connected');
else
    [~, gamepad_name] = GetGamepadIndices;
    gamepad_index = Gamepad('GetGamepadIndicesFromNames',gamepad_name);
    gp_numButtons = Gamepad('GetNumButtons', gamepad_index);
    % gamepad button map:
    % X = 1, A = 2
end;
gp_state_1 = Gamepad('GetButton', gamepad_index, 1);
gp_state_2 = Gamepad('GetButton', gamepad_index, 2);
[~, ~, keyCode] = KbCheck;
while ~keyCode(exitKey)
    while (~sum([gp_state_1, gp_state_2])) && ~keyCode(exitKey)
        gp_state_1 = Gamepad('GetButton', gamepad_index, 1);
        gp_state_2 = Gamepad('GetButton', gamepad_index, 2);
        [~, ~, keyCode] = KbCheck;
    end;
    fprintf('Button 1 = %d, Button 2 = %d\n',gp_state_1,gp_state_2)
    pause(0.1)
    gp_state_1=0; gp_state_2=0;
end
