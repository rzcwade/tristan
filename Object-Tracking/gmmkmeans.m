clc
close all;
clear all;

fr_ = imread('View_001/frame_0000.jpg');

fr_bw = rgb2gray(fr_); % convert frame to grayscale
fr_size = size(fr_);     fr_width = fr_size(2);      fr_height = fr_size(1);
fg = zeros(fr_height, fr_width);
bg_bw = zeros(fr_height, fr_width); 

% GMM Variables
C = 3; % number of gaussian components

% Create arrays to store 3 distributions
w = zeros(fr_height,fr_width,C); % initialize weights array
mean = zeros(fr_height,fr_width,C); % pixel means
sd = zeros(fr_height,fr_width,C); % pixel standard deviations
mean_diff = zeros(fr_height,fr_width,C); % difference of each pixel from mean
rank = zeros(1,C);


% Initialize component means and weights
[mean,sd,w] = initialization(fr_height, fr_width, mean, sd, w);

%create a empty avi file
v = VideoWriter('tracking_results.avi','Uncompressed AVI');
open(v)

% Process frames
srcFiles = dir('View_001\frame_*.jpg');
for n = 1:length(srcFiles)

    filename = strcat('C:/Users/zicheng/Documents/MATLAB/Objtracking/View_001/',srcFiles(n).name);
    fr = imread(filename);
	fr_bw = rgb2gray(fr); % convert frame to grayscale
    
    % Calculate diff of pixel from mean
    for m = 1:C
        mean_diff(:,:,m) = abs(bsxfun(@minus, double(fr_bw), double(mean(:,:,m))));
        %abs( double(fr_bw) - double(mean(:,:,m)) );
    end
    
    %output the foreground pixels
    fg = calcfg(fr_height,fr_width,sd,w,mean,mean_diff,fr_bw);     
    
    fg_ = im2bw(fg,0.1);
    s = regionprops(fg_,'BoundingBox','centroid');
    centroids = cat(1, s.Centroid);

    %figure(1), title(['Tracking Results:',num2str(n),'/',num2str(length(srcFiles))]),drawnow
    %subplot(1,2,1), imshow(fg_) 
    %subplot(1,2,2), imshow(fr) 
    figure(2), imshow(fr)
                    hold on 
                    plot(centroids(:,1),centroids(:,2), 'b*')
    
    F = getframe(gcf);
    %save as a avi file
    [X,Map] = frame2im(F);
    writeVideo(v,X)
    
end

close(v)
 

