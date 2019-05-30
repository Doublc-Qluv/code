import tensorflow as tf
import tensorflow.examples.tutorials.mnist.input_data as input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

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

loss_function = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=forward,labels=y))

train_epochs = 50
learning_rate = 0.01
display_step = 1 # 粒度
batch_size = 50
total_batch = int(mnist.train.num_examples/batch_size)#一轮的训练有多少批次

# 优化器
optimizer = tf.train.AdamOptimizer(learning_rate).minimize(loss_function)

correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(pred,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# train first
from time import time
startTime = time()

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

# 模型评估
accu_test = sess.run(
    accuracy,feed_dict={x:mnist.test.images, y:mnist.test.labels})
print("Test Accuracy: ",accu_test)