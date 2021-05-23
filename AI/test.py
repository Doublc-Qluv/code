from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
import random
import tensorflow as tf
from sklearn.model_selection import StratifiedKFold

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

'''# 构建和训练模型
def train_and_test(images_train, labels_train, images_test, labels_test, images_validation, labels_validation):
    pass


# 划分数据集并调用train_and_test测试和验证
def hold_out(images, labels, train_percentage):
    pass


def cross_validation(images, labels, k):
    pass
'''

# 使用简单划分的训练集和测试集训练，并使用测试集评估模型
# train_and_test(origin_images_train, origin_labels_train, origin_images_test, origin_labels_test, origin_images_test, origin_labels_test)

# 调用函数用留出法和k折交叉验证法评估模型
# hold_out(total_images, total_labels, 0.8)
# cross_validation(total_images, total_labels, 10)

inputLayer = tf.placeholder(tf.float32,[None,784],name="X")
outputLabel = tf.placeholder(tf.float32,[None,10],name="Y")

H1_NN = 256

W1 = tf.Variable(tf.random_normal([784,H1_NN]))
b1 = tf.Variable(tf.zeros([H1_NN]))

Y1 = tf.nn.relu(tf.matmul(inputLayer,W1) + b1)

W2 = tf.Variable(tf.random_normal([H1_NN,10]))
b2 = tf.Variable(tf.zeros([10]))

forward = tf.matmul(Y1,W2) + b2
pred = tf.nn.softmax(forward)

# # 神经网络中，权重通常初始化为正态分布随机数，b初始化为0
# W = tf.Variable(tf.random_normal([784,10]), name="W")
# b = tf.Variable(tf.zeros([10]), name="b")

# forward = tf.matmul(inputLayer,W) + b

# pred = tf.nn.softmax(forward)







# 构建和训练模型

train_loop = 50
batch_size = 100
#total_batch = int(mnist.train.num_examples / batch_size)
display_step = 5
learning_rate = 0.05

#loss_function = tf.reduce_mean(-tf.reduce_sum(outputLabel*tf.log(pred),reduction_indices=1))
loss_function = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=forward,labels=outputLabel))

optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss_function)


# 检查预测类别与实际类别的匹配情况 ， 参数1为第1维（按列），0则为按行，-1则为最后一维
correct_prediction = tf.equal(tf.argmax(pred,1), tf.argmax(outputLabel,1))

#准确率
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

def train_and_test(images_train, labels_train, images_test, labels_test, images_validation, labels_validation):
    
    total_batch = int(images_train.shape[0] / batch_size)
    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)
    
    for epoch in range(train_loop):
        for (batchImages, batchLabels) in batch_iter(images_train, labels_train, batch_size, train_loop, shuffle=True):
            batchImages, batchLabels = mnist.train.next_batch(batch_size)
            sess.run(optimizer,feed_dict={inputLayer: batchImages, outputLabel: batchLabels})

        # validate
        loss, acc = sess.run([loss_function,accuracy],
                            feed_dict={inputLayer: images_validation, outputLabel: labels_validation})
        
        # output
        if (epoch + 1) % display_step == 0:
            print("train epoch:%02d" % (epoch + 1), "Loss={:.9f}".format(loss),\
                 "accuracy: {:.4f}".format(acc))

    print("Train finished!")

    accu_test = sess.run(accuracy, feed_dict={inputLayer:images_test, outputLabel: labels_test})
    print("Test accuracy;",accu_test)
    return accu_test
    sess.close()



samp_images = {}
samp_labels = {}
for i in range(10):
    samp_images[i] = []
    samp_labels[i] = []
for i in range(total_images.shape[0]):
    num = get_label(total_labels[i])
    samp_images[num].append(total_images[i])
    samp_labels[num].append(total_labels[i])

# for i in range(10):
#     samp_images[i] = np.array(samp_images[i])
#     samp_labels[i] = np.array(samp_labels[i])
    
# samp_images: {  0:[[],[],[],...] , 1:[[],[],[]...] ....9:[[],[],[]...] }



def shuffle_samp(samp):
    #print(samp.shape)
    shuffle_indices = np.random.permutation(np.arange(samp.shape[0]))
    samp = samp[shuffle_indices]

# print(samp[1][0])



# 划分数据集并调用train_and_test测试和验证
def hold_out(train_percentage):
    
    n = 1
    accu = 0.0
    for i in range(n):
        print("loop %d" % i)
        
#         holdout_images_train = samp_images[0][0:2]
#         holdout_labels_train = samp_labels[0][0:2]
#         holdout_images_test = samp_images[0][-2:-1]
#         holdout_labels_test = samp_labels[0][-2:-1]
        holdout_images_train = []
        holdout_labels_train = []
        holdout_images_test = []
        holdout_labels_test = []
        
        
        print("beging generating the training and test set")
        # train set
        for num in range(10):
            num_of_batch = int(len(samp_images[num]) * train_percentage)
            
            holdout_images_train.extend(samp_images[num][:num_of_batch])
            holdout_labels_train.extend(samp_labels[num][:num_of_batch])
            holdout_images_test.extend(samp_images[num][num_of_batch:])
            holdout_labels_test.extend(samp_labels[num][num_of_batch:])

        holdout_images_train = np.array(holdout_images_train)
        holdout_labels_train = np.array(holdout_labels_train)
        holdout_images_test = np.array(holdout_images_test)
        holdout_labels_test = np.array(holdout_labels_test)
        
        shuffle_samp(holdout_images_train)
        shuffle_samp(holdout_labels_train)
        shuffle_samp(holdout_images_test)
        shuffle_samp(holdout_labels_test)
            
              
        accu += train_and_test(holdout_images_train, holdout_labels_train, holdout_images_test, holdout_labels_test, holdout_images_test, holdout_labels_test)


    print("after %d trainings,accuracy=" % n, accu / n)




def cross_validation(k=10):
    
    accu = 0.0
    
    image_groups = []
    label_groups = []
    
    
    for i in range(k):
        image_groups.append([])
        label_groups.append([])
        
    for i in range(10):
        
        group_len_of_this_num = len(samp_images[i]) // k
        
        ind= 0
        for j in range(k-1):
            image_groups[j].extend(samp_images[i][ind : ind + group_len_of_this_num])
            label_groups[j].extend(samp_labels[i][ind : ind + group_len_of_this_num])
            ind += group_len_of_this_num
        image_groups[k-1].extend(samp_images[i][ind:])
        label_groups[k-1].extend(samp_labels[i][ind:])
        
    
    for i in range(k):
        
        print("loop %d begins" % (i+1))
        
        cross_images_train = []
        cross_labels_train = []
        cross_images_test = []
        cross_labels_test = []
        
        cross_images_test.extend(image_groups[i])
        cross_labels_test.extend(label_groups[i])
        for j in range(k):
            if j != k:
                cross_images_train.extend(image_groups[j])
                cross_labels_train.extend(label_groups[j])
            
        cross_images_train = np.array(cross_images_train)
        cross_labels_train = np.array( cross_labels_train)
        cross_images_test = np.array(cross_images_test)
        cross_labels_test = np.array(cross_labels_test)
        
        shuffle_samp(cross_images_train)
        shuffle_samp(cross_labels_train)
        shuffle_samp(cross_images_test)
        shuffle_samp(cross_labels_test)
        
        
        accu += train_and_test(cross_images_train, cross_labels_train, cross_images_test, cross_labels_test, cross_images_test, cross_labels_test)

    
    print("after %d trainings,accuracy=" % k, accu / k)
    


    # 使用简单划分的训练集和测试集训练，并使用测试集评估模型
train_and_test(origin_images_train, origin_labels_train, origin_images_test, origin_labels_test, origin_images_test, origin_labels_test)


samp_images = {}
samp_labels = {}
for i in range(10):
    samp_images[i] = []
    samp_labels[i] = []
for i in range(total_images.shape[0]):
    num = get_label(total_labels[i])
    samp_images[num].append(total_images[i])
    samp_labels[num].append(total_labels[i])
def shuffle_samp(samp):
    #print(samp.shape)
    shuffle_indices = np.random.permutation(np.arange(samp.shape[0]))
    samp = samp[shuffle_indices]

# print(samp[1][0])


# 划分数据集并调用train_and_test测试和验证
def hold_out(train_percentage):
    
    n = 1
    accu = 0.0
    for i in range(n):
        print("loop %d" % i)
        holdout_images_train = []
        holdout_labels_train = []
        holdout_images_test = []
        holdout_labels_test = []
        print("beging generating the training and test set")
        # train set
        for num in range(10):
            num_of_batch = int(len(samp_images[num]) * train_percentage)
            holdout_images_train.extend(samp_images[num][:num_of_batch])
            holdout_labels_train.extend(samp_labels[num][:num_of_batch])
            holdout_images_test.extend(samp_images[num][num_of_batch:])
            holdout_labels_test.extend(samp_labels[num][num_of_batch:])
        holdout_images_train = np.array(holdout_images_train)
        holdout_labels_train = np.array(holdout_labels_train)
        holdout_images_test = np.array(holdout_images_test)
        holdout_labels_test = np.array(holdout_labels_test)  
        shuffle_samp(holdout_images_train)
        shuffle_samp(holdout_labels_train)
        shuffle_samp(holdout_images_test)
        shuffle_samp(holdout_labels_test)         
        accu += train_and_test(holdout_images_train, holdout_labels_train, \
            holdout_images_test, holdout_labels_test, holdout_images_test, holdout_labels_test)
    print("after %d trainings,accuracy=" % n, accu / n)

def cross_validate(session, split_size=20):
    results = []
    kf = KFold(n_splits=split_size)
    for train_idx, val_idx in kf.split(train_x_all, train_y_all):
        train_x = train_x_all[train_idx]
        train_y = train_y_all[train_idx]
        val_x = train_x_all[val_idx]
        val_y = train_y_all[val_idx]
        train_and_test(session, train_x, train_y)
        results.append(session.run(accuracy, feed_dict={x: val_x, y: val_y}))
    return results