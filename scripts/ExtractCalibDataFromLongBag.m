% Copyright (C) 2022, IADC, Hong Kong University of Science and Technology
% Copyright (C) 2022, RPL, KTH Royal Institute of Technology
% Authors: Kin ZHANG qingwen@kth.se, Tianshuai HU thuaj@connect.ust.hk

% Reference link: https://ww2.mathworks.cn/help/lidar/ug/read-lidar-and-camera-data-from-rosbag.html
% Date: 2022/12/13
% Description: 
% - Extract the bag data to image and point cloud for calibration on extrinsic
% - Make any change if you want and leave these comments
% - This scripts require at least 3 seconds that no moving object in the
% - image!!! Make sure about this requirement otherwise it will fail to extract

%% =======> Things you need change based on your path and topic name <======
clc,clear

bag_folder = "D:\Users\24397\Documents\AProgram\calib_test\";
save_folder = "D:\Users\24397\Documents\AProgram\calib_test\kin_whole_extract\";

bag_name = "forqingwen_2022-12-13-13-53-14.bag";
image_topic_name = "/camera/color/image_raw/compressed";
point_cloud_topic_name = "/rslidar_points";

% config of extraction
numFrameSave = 50; % note: the number will be smaller than this one since static frame skip
time_toleration = 0.05;
Dyn_threshold = 0.001; % ratio in (the image dynamic)*100 => default one is enough


%% below is automatically extract step
fprintf('====== Starting AUTO Extraction ======\n');
tStart = tic;
path = bag_folder + bag_name;
bag = rosbag(path);
imageBag = select(bag,'Topic',image_topic_name);
pcBag = select(bag,'Topic',point_cloud_topic_name);

imageMsgs = readMessages(imageBag);
pcMsgs = readMessages(pcBag);

ts1 = timeseries(imageBag);
ts2 = timeseries(pcBag);
t1 = ts1.Time;
t2 = ts2.Time;

% For accurate calibration, images and point clouds must be captured with the same timestamps. 
% Match the corresponding data from both the sensors according to their timestamps. 
% To account for uncertainty, use a margin of 0.1 seconds.
k = 1;
if size(t2,1) > size(t1,1)
for i = 1:size(t1,1)
    [val,indx] = min(abs(t1(i) - t2));
    if val <= time_toleration
        idx(k,:) = [i indx];
        k = k + 1;
    end
end
else
for i = 1:size(t2,1)
    [val,indx] = min(abs(t2(i) - t1));
    if val <= time_toleration
        idx(k,:) = [indx i];
        k = k + 1;
    end
end   
end
%%
imageFilesPath = save_folder +'imgs';
pcFilesPath = save_folder +'pcds';
if ~exist(imageFilesPath, 'dir')
    mkdir(imageFilesPath);
    fprintf('%s mkdir oh this folder.\n',imageFilesPath);
end
if ~exist(pcFilesPath, 'dir')
    mkdir(pcFilesPath);
    fprintf('%s mkdir oh this folder.\n',pcFilesPath);
end

if k == 1
    fprintf(2, "NO MATCHING DATA FRAME!! Kill the code\n")
    fprintf("Note: please tune bigger of `time_toleration`, now is %f\n", time_toleration);
    return
end
fprintf("After sync, total frames in your dataset: %d \n", length(idx));
fprintf("But we will only save : %d as you set\n", numFrameSave);
index_threshold = fix(length(idx)/numFrameSave) - fix(length(idx)/(5*numFrameSave)); % two data index difference need over this

%%
p_img = -1;
p_i = -1;
extract_len = length(idx); % only for debug
% extract_len = 100; % only for debug
for i = 1:extract_len
    I = readImage(imageMsgs{idx(i,1)});
    % make sure previous images have data
    if p_img == -1
        p_img = I;
        p_i = i;
        continue
    end
    K = rgb2gray(imabsdiff(p_img,I));
    % hard code here TODO set threshold??
    NotZeros = sum(sum(K>50));
    Zeros = sum(sum(K<50));
    Dyna_ratio = NotZeros/(NotZeros+Zeros) * 100;
    is_static2img = (Dyna_ratio<Dyn_threshold);

    if ~is_static2img || abs(p_i-i)<index_threshold
%         fprintf('\n skip this frame: %d p_i:%d i:%d \n',Dyna_ratio,p_i,i);
        p_img = I;
        continue
    end
    pc = pointCloud(readXYZ(pcMsgs{idx(i,2)}));
    n_strPadded = sprintf( '%04d', i ) ;
    pcFileName = strcat(pcFilesPath,'/', n_strPadded, '.pcd');
    imageFileName = strcat(imageFilesPath,'/', n_strPadded, '.png');
    imwrite(I, imageFileName);
    pcwrite(pc, pcFileName);
    p_img = I;
    p_i = i;
end
%%
tEnd = toc(tStart);
SavedfilesNum = numel(dir(imageFilesPath+'\*.png'));
fprintf('\nTotal time cost: %f s \n All extract process is done. Check folder for your data: \n %s, \n %s\n',tEnd, imageFilesPath, pcFilesPath);
fprintf(' There should be <strong>%d </strong>images and pcds inside each folder. \n', SavedfilesNum);
fprintf('====== Finished Extraction ======\n');

