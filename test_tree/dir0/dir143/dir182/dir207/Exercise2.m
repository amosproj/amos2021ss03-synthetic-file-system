%task a

toy1 = imread('toycars1.png');
toy2 = imread('toycars2.png');
toy1BW = im2bw(toy1, 0.5);
toy2BW = im2bw(toy2, 0.5);

figure, subplot(2, 4 ,1), imshow(toy1BW);
subplot(2, 4 ,2), imshow(toy2BW);

%task b

orProduct = toy1BW | toy2BW;
andProduct = toy1BW & toy2BW;
XorProduct = xor(toy1BW, toy2BW);

subplot(2, 4 ,3), imshow(orProduct);
subplot(2, 4 ,4), imshow(XorProduct);
subplot(2, 4 ,5), imshow(andProduct);

%task c

load trees
BW = im2bw(X, map, 0.1);

subplot(2, 4 ,6), imshow(X,map);
subplot(2, 4 ,6), imshow(BW);