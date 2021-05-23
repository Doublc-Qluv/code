import tensorflow as tf
import tensorflow.examples.tutorials.mnist.input_data as input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

#28 * 28 = 784
x = tf.placeholder(tf.float32,[None,784],name="X")
y = tf.placeholder(tf.float32,[None,10],name="Y")
W = tf.Variable(tf.random_normal([784,10]),name="W")
b = tf.Variable(tf.zeros([10]),name="b")
train_epochs = 10
learning_rate = 0.05
display_step = 10
batch_size = 10
total_batch = 100

forward = tf.matmul(x, W) + b
pred = tf.nn.softmax(forward)# softmax分类
loss_function = tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred),reduction_indices=1))#交叉熵

optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss_function)#梯度下降

# 检查预测类别tf.argmax(pred,1)与实际类别tf.argmax(y,1)的匹配情况
correct_prediction = tf.equal(tf.argmax(pred,1),tf.argmax(y,1))
# 准确率，将布尔值转化为浮点数，并计算平均值
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)

for epoch in range(train_epochs):
    for batch in range(total_batch):
        xs ,ys = mnist.train.next_batch(batch_size)
        sess.run(optimizer,feed_dict={x:xs,y:ys})

    loss,acc = sess.run([loss_function,accuracy],feed_dict={x:mnist.validation.images, y:mnist.validation.labels})
    #print
    if (epoch+1)%display_step == 0:
        print("Train Epoch:", "%02d"%(epoch+1),"Loss=","{:.9f}".format(loss),\
            "Accuracy= ","{:.4f}".format(acc))
print("Train Finished")


'''
accu_test = sess.run(accuracy,feed_dict={mnist.test.images, \
    y:mnist.test.labels})
print("Test Accuracy: ",accu_test)
'''