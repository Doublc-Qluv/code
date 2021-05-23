from sklearn.model_selection import KFold,StratifiedKFold
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# 参数
learning_rate = 0.02
batch_size = 500
epoch_num = 10 #训练的迭代次数

# TF graph

#数据和标签的占位
x = tf.placeholder(tf.float32, [None, 784])
y = tf.placeholder(tf.float32, [None, 10])

W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
pred = tf.nn.softmax(tf.matmul(x, W) + b)
cost = tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred), reduction_indices=1))
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

#测试阶段，测试准确度计算
correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
init = tf.global_variables_initializer()

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
train_x_all = mnist.train.images
train_y_all = mnist.train.labels
test_x = mnist.test.images
test_y = mnist.test.labels


def run_train(session, train_x, train_y):
    print("\nStart training")
    session.run(init)
    for epoch in range(epoch_num):
        total_batch = int(train_x.shape[0] / batch_size)
        for i in range(total_batch):
            batch_x = train_x[i*batch_size:(i+1)*batch_size]
            batch_y = train_y[i*batch_size:(i+1)*batch_size]
            _, c = session.run([optimizer, cost], feed_dict={x: batch_x, y: batch_y})
            if i % 50 == 0:
                print("Epoch #%d step=%d loss_value=%f" % (epoch, i, c))
                print("accuracy:{}".format(session.run(accuracy,feed_dict={x: mnist.test.images, y: mnist.test.labels})))
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
#交叉验证
def cross_validate(session, split_size=10):
    results = []
    kf = StratifiedKFold(n_splits=split_size)
    for train_idx, val_idx in kf.split(train_x_all, train_y_all.argmax(1)+1):
        train_x = train_x_all[train_idx]
        train_y = train_y_all[train_idx]
        val_x = train_x_all[val_idx]
        val_y = train_y_all[val_idx]
        run_train(session, train_x, train_y)
        results.append(session.run(accuracy, feed_dict={x: val_x, y: val_y}))
    return results

with tf.Session() as session:
    result = cross_validate(session)
    print("Cross-validation result: %s" % result)
    print("Test accuracy: %f" % session.run(accuracy, feed_dict={x: test_x, y: test_y}))