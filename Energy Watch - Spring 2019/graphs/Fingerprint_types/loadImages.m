folders = {'1_Same','2_Concentric','3_People','4_Schedule','5_Reverse','6_Random'};
names = {'same';'concentric';'people';'schedule';'reverse';'random'};

%Read all training images
cd Training;
train_images = [];
train_labels = [];
train_units = [];
for f = 1:length(folders)
    cd (folders{f});
    list = ls;
    [r,c] = size(list);
    for i = 3:r
        img = imread(list(i,:));
        %Get the unit value for each image
        label = img(20:40,70:95);
        mask = label >= 10;
        label(mask) = 255;
        train_units = cat(4,train_units,label);
        %Resize the image to be used for training and save image and
        %classification
        img = imresize(img,[30,44]);
        train_images = cat(4,train_images,img);
        train_labels = [train_labels;f];
    end
    cd ../;
end
train_labels = categorical(train_labels');
%Randomize the images and labels
len = length(train_labels);
inds = randperm(len);
train_images = train_images(:,:,:,inds);
train_labels = train_labels(inds);
train_units = train_units(:,:,:,inds);

cd ../
%Read all testing images
cd Testing;
test_images = [];
test_labels = [];
test_units = [];
for f = 1:length(folders)
    cd (folders{f});
    list = ls;
    [r,c] = size(list);
    for i = 3:r
        img = imread(list(i,:));
        %Get the unit value for each image
        label = img(20:40,70:95);
        mask = label >= 10;
        label(mask) = 255;
        test_units = cat(4,test_units,label);
        %Resize the image to be used for testing and save image and
        %classifcation
        img = imresize(img,[30,44]);
        test_images = cat(4,test_images,img);
        test_labels = [test_labels;f];
    end
    cd ../;
end
cd ../;
test_labels = categorical(test_labels);
%Randomize the images and labels
len = length(test_labels);
inds = randperm(len);
test_images = test_images(:,:,:,inds);
test_labels = test_labels(inds);
test_units = test_units(:,:,:,inds);


%Create neural network, train it, and test it
layers = [imageInputLayer([30 44 3]);
    convolution2dLayer(3,96,'Stride',1,'Padding',1);
    reluLayer();
    dropoutLayer();
    maxPooling2dLayer(3,'Stride',2);
    convolution2dLayer(3,192,'Stride',1,'Padding',1);
    reluLayer();
    dropoutLayer();
    maxPooling2dLayer(3,'Stride',2);
    convolution2dLayer(3,384,'Stride',1,'Padding',1);
    reluLayer();
    dropoutLayer();
    maxPooling2dLayer(3,'Stride',2);
    fullyConnectedLayer(2048);
    reluLayer();
    dropoutLayer();
    fullyConnectedLayer(6);
    softmaxLayer();
    classificationLayer()];
options = trainingOptions('sgdm','MaxEpochs',10,'MiniBatchSize',5,'InitialLearnRate',0.001);
fingerConvnet = trainNetwork(train_images, train_labels, layers, options);
pred = classify(fingerConvnet,test_images);
accuracy = sum(pred == test_labels)/numel(test_labels)