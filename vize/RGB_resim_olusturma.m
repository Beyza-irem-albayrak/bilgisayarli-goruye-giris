
rows = 256;
cols = 256;

[x, y] = meshgrid(1:cols, 1:rows);

cx = cols / 2;
cy = rows / 2;

R = uint8(255 * (sqrt((x - cx).^2 + (y - cy).^2) <= 64));
G = uint8(255 * (sqrt((x - cx).^2 + (y - cy).^2) <= 96));
B = uint8(255 * (sqrt((x - cx).^2 + (y - cy).^2) <= 128));

imageRGB = cat(3, R, G, B);

figure;
imshow(imageRGB);
title('Çembersel Fonksiyon ile Oluşturulan RGB Görüntü (64-96-128 Yarıçap)');

% 2D Contourf Grafikler (Her kanal için)

figure;
contourf(x, y, R, 'LineColor', 'none');
colormap('autumn');
title('R Kanalı (64 px) - 2D Kontur Grafiği');
xlabel('x'); ylabel('y');

figure;
contourf(x, y, G, 'LineColor', 'none');
colormap('summer');
title('G Kanalı (96 px) - 2D Kontur Grafiği');
xlabel('x'); ylabel('y');

figure;
contourf(x, y, B, 'LineColor', 'none');
colormap('winter');
title('B Kanalı (128 px) - 2D Kontur Grafiği');
xlabel('x'); ylabel('y');

% 3D Mesh Grafikler (Her kanal için)

figure;
mesh(x, y, double(R));
title('R Kanalı - 3D Mesh (64 px)');
xlabel('x'); ylabel('y'); zlabel('R Değeri');

figure;
mesh(x, y, double(G));
title('G Kanalı - 3D Mesh (96 px)');
xlabel('x'); ylabel('y'); zlabel('G Değeri');

figure;
mesh(x, y, double(B));
title('B Kanalı - 3D Mesh (128 px)');
xlabel('x'); ylabel('y'); zlabel('B Değeri');
