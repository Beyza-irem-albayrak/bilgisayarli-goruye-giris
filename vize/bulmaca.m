
pkg load image;

function pieces = split_image(img, rows, cols)
  [height, width, ~] = size(img);
  piece_height = floor(height / rows);
  piece_width = floor(width / cols);

  pieces = cell(rows, cols);
  for i = 1:rows
    for j = 1:cols
      pieces{i, j} = img((i-1)*piece_height + 1:i*piece_height, ...
                         (j-1)*piece_width + 1:j*piece_width, :);
    end
  end
end

function new_img = shuffle_pieces(pieces)
  [rows, cols] = size(pieces);
  indices = randperm(rows * cols);

  shuffled_pieces = cell(rows, cols);
  for k = 1:length(indices)
    i = ceil(indices(k) / cols);
    j = mod(indices(k) - 1, cols) + 1;
    shuffled_pieces{k} = pieces{i, j};
  end

  [piece_height, piece_width, ~] = size(pieces{1, 1});
  new_img = zeros(piece_height * rows, piece_width * cols, 3, 'uint8');
  for i = 1:rows
    for j = 1:cols
      new_img((i-1)*piece_height + 1:i*piece_height, ...
              (j-1)*piece_width + 1:j*piece_width, :) = shuffled_pieces{(i-1)*cols + j};
    end
  end
end

output_dir = 'C:/Users/BEYZA İREM ALBAYRAK/OneDrive/Masaüstü/sonuclar/';
if ~exist(output_dir, 'dir')
  mkdir(output_dir);
end

img = imread("C:/Users/BEYZA İREM ALBAYRAK/OneDrive/Masaüstü/resim1.jpg"); % Dosya yolunu doğru ayarlayın

rows = 3;
cols = 3;

pieces = split_image(img, rows, cols);

for version = 1:3
    shuffled_img = shuffle_pieces(pieces);

    output_filename = sprintf('%sshuffled_img_3x3_version_%d.jpg', output_dir, version);
    imwrite(shuffled_img, output_filename);
end

disp(['Sonuçlar ', output_dir, ' dizinine kaydedildi.']);
dir(output_dir);





