a = imread('cola1.png');
b= imread('cola2.png');

figure, subplot(2, 2, 1), imshow(a);
subplot(2, 2, 2), imshow(b);

d = b-a;
subplot(2, 2, 3), imshow(d);

c = imabsdiff(b,a); %Use function imabsdiff
subplot(2, 2, 4), imshow(c);

% task B:
%{
	The cola2 is brighter than the cola1, so the value of every element in the image matrix of cola2 is bigger than that of cola1. Therefore, when we do the subtraction cola2 – cola1, the image result is just like the picture cola2 and cola1 but darker than them.
	The application of this is to check the difference of two images.
%}

% task C:
%{
	Imabsdiff: Absolute difference of two images.
	Z = imabsdiff(x, y) subtracts each element in array Y from the corresponding element in array X and returns the absolute difference in the corresponding element of the output Z.
%}
