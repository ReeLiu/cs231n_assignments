import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  scoresOfN = np.dot(X,W)
  dataLoss = 0	
  for i in range(X.shape[0]):
	groundTruth = y[i]
	scores = scoresOfN[i]
	scores -= np.max(scores)#trcik for stabiltiy
	pros = np.exp(scores)/np.sum(np.exp(scores))
	groudTruthLoss = -np.log(pros[groundTruth])
	dataLoss += groudTruthLoss
	#for W_groudTruth, gradient (P_groundTruth - 1)*X_i
	#for W_j(j != groundTruth), gradient is (P_j)*X_i
 	Y = np.zeros(W.shape[1])
	Y[groundTruth] = 1
	sample = X[i]
	data_gradient = np.multiply(sample[:,np.newaxis],(pros - Y))
	#gradient for Regularization loss
	R_gradient  = 2*reg*W
	dW_i = data_gradient + R_gradient
	dW += dW_i

  RLoss = np.sum(np.square(W))
  dataLoss = dataLoss/X.shape[0]
  loss = dataLoss + reg*RLoss 	
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################
  #the gradient of a batch is the average of gradients of samples in the batch
  return loss, dW/X.shape[0]


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  scores = np.dot(X,W)
  rescaled_scores = scores - np.max(scores,axis = 1)[:,np.newaxis]
  s_scores = np.exp(rescaled_scores)
  probs = np.divide(s_scores,np.sum(s_scores,axis = 1)[:,np.newaxis])
  ground_truth_probs = probs[range(X.shape[0]),y]
  ground_truth_probs[ground_truth_probs <=0] = 10**-10
  data_loss = np.sum(-np.log(ground_truth_probs))/X.shape[0]
  reg_loss = np.sum(np.square(W))
  loss = data_loss + reg_loss
    
  masks = np.zeros_like(probs)
  masks[range(X.shape[0]),y] = 1
  intermedia = probs - masks
  #data_gradients = np.sum(np.multiply(intermedia[:,:,np.newaxis],X[:,np.newaxis]),axis = 0)/X.shape[0]
  data_gradients = np.dot(X.T,intermedia).T/X.shape[0]
  re_gradients = 2*reg*W
  dW = data_gradients.T +re_gradients	 			
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

