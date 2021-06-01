coins = imread('coins.png');
figure, subplot(2, 3, 1), imshow(coins);
subplot(2, 3, 2), imhist(coins);

level = graythresh(coins);
ex4BW = im2bw(coins, level);
subplot(2, 3, 3), imshow(ex4BW);

coinsStretch = imadjust(coins,stretchlim(coins, [0.05 0.95]),[]);
subplot(2, 3, 4), imshow(coinsStretch); 
subplot(2, 3, 5), imhist(coinsStretch);