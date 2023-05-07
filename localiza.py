import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

def color_indexing(database, query, bin_size):
    """
    Retorna as imagens mais similares à consulta de acordo com o algoritmo de indexação por cor proposto por Swain & Ballard.

    Args:
    - database (list): lista de imagens de entrada, cada imagem é uma matriz numpy 3D (altura x largura x 3) de valores RGB.
    - query (numpy.ndarray): matriz numpy 3D (altura x largura x 3) de valores RGB que representa a imagem de consulta.
    - bin_size (int): tamanho do bin utilizado na quantização da imagem.

    Returns:
    - ordered_images (list): lista ordenada de imagens mais similares à consulta.
    """
    # Quantização da imagem de consulta
    # query_bins = quantize_image(query, bin_size)

    # Cálculo dos histogramas das imagens do banco de dados
    hist_list = []
    for image in database:
        hist = calculate_histogram(image, bin_size)
        hist_list.append(hist)

    query_bins = calculate_histogram(query, bin_size)

    # Cálculo das similaridades entre a imagem de consulta e as imagens do banco de dados
    sim_list = []
    for hist in hist_list:
        sim = calculate_similarity(query_bins, hist)
        sim_list.append(sim)

    # Ordenação das imagens do banco de dados de acordo com a similaridade
    ordered_images = [database[i] for i in np.argsort(sim_list)[::-1]]

    return ordered_images, sim_list

def quantize_image(image, bin_size):
    """
    Quantiza a imagem em bins de tamanho bin_size.

    Args:
    - image (numpy.ndarray): matriz numpy 3D (altura x largura x 3) de valores RGB.
    - bin_size (int): tamanho do bin utilizado na quantização.

    Returns:
    - bins (numpy.ndarray): matriz numpy 2D (altura * largura x 3) de valores RGB quantizados.
    """
    height, width, _ = image.shape
    bins = np.reshape(image, (height * width, 3))
    bins = np.floor_divide(bins, bin_size)
    return bins

def calculate_histogram(image, bin_size):
    """
    Calcula o histograma de uma imagem quantizada em bins de tamanho bin_size.

    Args:
    - image (numpy.ndarray): matriz numpy 3D (altura x largura x 3) de valores RGB.
    - bin_size (int): tamanho do bin utilizado na quantização.

    Returns:
    - hist (numpy.ndarray): vetor numpy 1D de tamanho (bin_size ** 3) representando o histograma da imagem.
    """
    bins = quantize_image(image, bin_size)
    hist, _ = np.histogramdd(bins, bins=[bin_size, bin_size, bin_size])
    return hist.flatten()

def calculate_similarity(hist1, hist2):
    """
    Calcula a similaridade entre dois histogramas.

    Args:
    - hist1 (numpy.ndarray): vetor numpy 1D representando o primeiro histograma.
    - hist2 (numpy.ndarray): vetor numpy 1D representando o segundo histograma.

    Returns:
    - sim (float): valor de similaridade entre os histogramas.
    """
    return np.dot(hist1, hist2) / (np.linalg.norm(hist1) * np.linalg.norm(hist2))

# diretório com as imagens
img_dir = './imagens/'

# lista de imagens
images = []

# loop pelos arquivos no diretório
for filename in os.listdir(img_dir):
    # lendo a imagem
    img = Image.open(os.path.join(img_dir, filename))
    # convertendo para matriz numpy e adicionando à lista
    images.append(np.array(img))

# abre a imagem de consulta em formato JPEG
query_image = Image.open('query.jpg')

# converte a imagem para uma matriz numpy
query_image = np.asarray(query_image)

ordered_images, sim_list = color_indexing(database=images, query=query_image, bin_size=16)

num_images = 5

fig, axs = plt.subplots(2, 3, figsize=(12, 8))
for i in range(num_images):
    row = i // 3
    col = i % 3
    axs[row, col].imshow(ordered_images[i])
    axs[row, col].set_title(f"Similarity: {sim_list[i]:.2f}")
    axs[row, col].axis('off')

plt.show()