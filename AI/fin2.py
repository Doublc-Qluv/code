from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
import random

# 将 numpy 数组中的图片和标签顺序打乱
def shuffer_images_and_labels(images, labels):
    shuffle_indices = np.random.permutation(np.arange(len(images)))
    shuffled_images = images[shuffle_indices]
    shuffled_labels = labels[shuffle_indices]
    return shuffled_images, shuffled_labels

# 将label从长度10的one hot向量转换为0~9的数字
# 例：get_label(total_labels[0]) 获取到total_labels中第一个标签对应的数字
def get_label(label):
    return np.argmax(label)

# images：训练集的feature部分
# labels：训练集的label部分
# batch_size： 每次训练的batch大小
# epoch_num： 训练的epochs数
# shuffle： 是否打乱数据
# 使用示例：
#   for (batchImages, batchLabels) in batch_iter(images_train, labels_train, batch_size, epoch_num, shuffle=True):
#       sess.run(feed_dict={inputLayer: batchImages, outputLabel: batchLabels})
def batch_iter(images,labels, batch_size, epoch_num, shuffle=True):
    
    data_size = len(images)
    
    num_batches_per_epoch = int(data_size / batch_size)  # 样本数/batch块大小,多出来的“尾数”，不要了
    
    for epoch in range(epoch_num):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            
            shuffled_data_feature = images[shuffle_indices]
            shuffled_data_label   = labels[shuffle_indices]
        else:
            shuffled_data_feature = images
            shuffled_data_label = labels

        for batch_num in range(num_batches_per_epoch):   # batch_num取值0到num_batches_per_epoch-1
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)

            yield (shuffled_data_feature[start_index:end_index] , shuffled_data_label[start_index:end_index])


# 读取数据集
mnist = input_data.read_data_sets('./mnist_dataset', one_hot=True)

total_images = mnist.train.images
total_labels = mnist.train.labels
total_images, total_labels = shuffer_images_and_labels(total_images, total_labels)

# 简单划分前50000个为训练集，后5000个为测试集
origin_images_train = total_images[:50000]
origin_labels_train = total_labels[:50000]
origin_images_test = total_images[50000:]
origin_labels_test = total_labels[50000:]

# 构建和训练模型
def train_and_test(images_train, labels_train, images_test, labels_test, images_validation, labels_validation):
    pass


# 划分数据集并调用train_and_test测试和验证
def hold_out(images, labels, train_percentage):
    pass


def cross_validation(images, labels, k):
    pass


# 使用简单划分的训练集和测试集训练，并使用测试集评估模型
# train_and_test(origin_images_train, origin_labels_train, origin_images_test, origin_labels_test, origin_images_test, origin_labels_test)

# 调用函数用留出法和k折交叉验证法评估模型
# hold_out(total_images, total_labels, 0.8)
# cross_validation(total_images, total_labels, 10)