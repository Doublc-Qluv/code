from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import numpy as np
import random
from time import time

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
mnist = input_data.read_data_sets('./MNIST_data/', one_hot=True)

total_images = mnist.train.images
total_labels = mnist.train.labels
total_images, total_labels = shuffer_images_and_labels(total_images, total_labels)

# 简单划分前50000个为训练集，后5000个为测试集
origin_images_train = total_images[:50000]
origin_labels_train = total_labels[:50000]
origin_images_test = total_images[50000:]
origin_labels_test = total_labels[50000:]

# 构建和训练模型
# 构建和训练模型
def train_and_test(images_train, labels_train, 
                   images_test, labels_test, 
                   images_validation, 
                   labels_validation):
    x = tf.placeholder(tf.float32,[None,784], name="X")
    y = tf.placeholder(tf.float32,[None,10], name="Y")
    
    H1_NN = 256
    H2_NN = 64
    # 输入层-隐藏层1
    W1 = tf.Variable(tf.truncated_normal([784,H1_NN],stddev=0.1))
    b1 = tf.Variable(tf.zeros([H1_NN]))

    # 隐藏层1-隐藏层2
    W2 = tf.Variable(tf.truncated_normal([H1_NN,H2_NN],stddev=0.1))
    b2 = tf.Variable(tf.zeros([H2_NN]))

    # 隐藏层2-输出层
    W3 = tf.Variable(tf.truncated_normal([H2_NN,10],stddev=0.1))
    b3 = tf.Variable(tf.zeros([10]))

    # 隐藏层1结果
    Y1 = tf.nn.relu(tf.matmul(x, W1) + b1)

    # 隐藏层2结果
    Y2 = tf.nn.relu(tf.matmul(Y1, W2) + b2)

    # 输出层结果
    forward = tf.matmul(Y2, W3) + b3
    pred = tf.nn.softmax(forward)
    loss_function = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=forward,labels=y))
    
    train_epochs = 50
    learning_rate = 0.01
    display_step = 1 # 粒度
    batch_size = 50
    total_batch = int(mnist.train.num_examples/batch_size)#一轮的训练有多少批次

    # 优化器
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(loss_function)
    
    correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(pred,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    for epoch in range(train_epochs):
        for batch in range(total_batch):
            xs,ys = mnist.train.next_batch(batch_size)
            sess.run(optimizer, feed_dict={x:xs,y:ys})

        loss,acc = sess.run([loss_function,accuracy],
                           feed_dict={x:mnist.validation.images,
                                     y:mnist.validation.labels})


        if (epoch+1) % display_step == 0:
            print("Train Epoch:","%02d"%(epoch+1),
                 "Loss=","{:.9f}".format(loss),"Accuracy=","{:.4f}".format(acc))
    duration = time()-startTime
    print("Train Finished takes:","{:.2f}".format(duration))
    
train_and_test(origin_images_train, origin_labels_train, 
               origin_images_test, origin_labels_test, origin_images_test, origin_labels_test)

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