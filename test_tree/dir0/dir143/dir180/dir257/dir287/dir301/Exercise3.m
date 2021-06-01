cameraMan = imread('cameraman.tif');
figure, subplot(3, 4, 1), imshow(cameraMan);

Id = im2double(cameraMan);
newId = 2* log(1+Id);
subplot(3, 4, 2), imshow(newId);

alpha = 0.3;
newExpo = 4 * ((1+alpha).^Id - 1);
subplot(3, 4, 3), imshow(newExpo);

alpha = 0.4;
newExpo = 4 * ((1+alpha).^Id - 1);
subplot(3, 4, 4), imshow(newExpo);

alpha = 0.6;
newExpo = 4 * ((1+alpha).^Id - 1);
subplot(3, 4, 5), imshow(newExpo);

beta = 0.5;
gammaCorrect = 2 * Id.^beta;
subplot(3, 4, 6), imshow(gammaCorrect);

beta = 1.5;
gammaCorrect = 2 * Id.^beta;
subplot(3, 4, 7), imshow(gammaCorrect);

beta = 3;
gammaCorrect = 2 * Id.^beta;
subplot(3, 4, 8), imshow(gammaCorrect);

gaCo = imadjust(cameraMan, [0; 1], [0; 1], 1/0.5);
subplot(3, 4, 9), imshow(gaCo);

gaCo = imadjust(cameraMan, [0; 1], [0; 1], 1/1.5);
subplot(3, 4, 10), imshow(gaCo);

gaCo = imadjust(cameraMan, [0; 1], [0; 1], 1/3);
subplot(3, 4, 11), imshow(gaCo);
