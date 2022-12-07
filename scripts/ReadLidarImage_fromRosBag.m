% Origin one from Copyright 2020 The MathWorks, Inc. 
% Reference link: https://ww2.mathworks.cn/help/lidar/ug/read-lidar-and-camera-data-from-rosbag.html
% Date: 2022/12/7
% Description: 
% - Make a little change and TODO auto extraction directly to calib
% - Extract the bag data to image and point cloud for calibration on extrinsic
% - Make any change if you want and leave these comments
% Copyright (C) 2022, IADC, Hong Kong University of Science and Technology
% Copyright (C) 2022, RPL, KTH Royal Institute of Technology
% Authors: Tianshuai HU thuaj@connect.ust.hk, Kin ZHANG qzhangcb@connect.ust.hk
clc,clear
% Things you need change based on your path and topic name
bag_folder = "D:\Users\24397\Documents\AProgram\calib_test\";
save_folder = "D:\Users\24397\Documents\AProgram\calib_test\"; % will create pcd and img folder
bag_name = "calib02_2022-12-05-22-04-07.bag";
image_topic_name = "/camera/color/image_raw/compressed";
point_cloud_topic_name = "/rslidar_points";
time_toleration = 0.01;
% Things you need change based on your path and topic name


%% below is automatically extract step
fprintf('====== Starting Extraction ======\n');
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
fprintf("After sync, total frames in your folder: %d \n", length(idx));

for i = 1:length(idx)
        I = readImage(imageMsgs{idx(i,1)});
        pc = pointCloud(readXYZ(pcMsgs{idx(i,2)}));
        n_strPadded = sprintf( '%04d', i ) ;
        pcFileName = strcat(pcFilesPath,'/', n_strPadded, '.pcd');
        imageFileName = strcat(imageFilesPath,'/', n_strPadded, '.png');
        imwrite(I, imageFileName);
        pcwrite(pc, pcFileName);
end

%%
tEnd = toc(tStart);
fprintf('Total time cost: %f s \n All extract process is done. Check folder for your data: \n %s, \n %s\n',tEnd, imageFilesPath, pcFilesPath);
fprintf("ATTENTION! Maybe it still need some selection on your dataset and then send to the calibration tool\n");
fprintf('====== Finished Extraction ======\n');
