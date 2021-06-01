peppers = imread('peppers.png');
hsv_peper = rgb2hsv(peppers);

hue = hsv_peper(:,:,1); %Hue image
saturation = hsv_peper(:,:,2); %Staturation image
value = hsv_peper(:,:,3); %Indensity image

figure, subplot(3, 3, 1), imshow(peppers);
subplot(3, 3, 2), imshow(hsv_peper);
subplot(3, 3, 4), imshow(hue);
subplot(3, 3, 5), imshow(saturation);
subplot(3, 3, 6), imshow(value);

yiq_peper = rgb2ntsc(peppers);

lumi = yiq_peper(:,:,1);
inten = yiq_peper(:,:,2);
chromi = yiq_peper(:,:,3);

subplot(3,3,7), imshow(lumi);
subplot(3,3,8), imshow(inten);
subplot(3,3,9), imshow(chromi);