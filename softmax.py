from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange

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
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_train = X.shape[0]
    num_classes = W.shape[1]
    scores=X @ W
    normal_scores=scores-np.max(scores,axis=1,keepdims=True)
    exp_scores=np.exp(normal_scores)
    exp_scores_sum=np.sum(exp_scores,axis=1)
    for i in range(num_train):
        loss+=-np.log(exp_scores[i,y[i]]/exp_scores_sum[i])
        for j in range(num_classes):
            dW[:,j]+=X[i]*exp_scores[i,j]/exp_scores_sum[i]
            if j==y[i]:
                dW[:,j]-=X[i]
    loss=loss/num_train+reg * np.sum(np.square(W))
    dW=dW/num_train+2*reg*W
    #
    # for i in range(num_train):
    #     loss -= np.log(exp_scores[i, y[i]])
    #     for j in range(X.shape[1]):
    #         for k in range(num_classes):
    #             dW[j, k] += exp_scores[i, k] * X[i, j]
    #             if k == y[i]:
    #                 dW[j, k] -= X[i, j]
    # loss = loss / num_train +  reg * np.sum(np.square(W))
    # dW = dW / num_train + reg * W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


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
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    num_train = X.shape[0]
    scores=X.dot(W)
    scores=scores-np.max(scores,axis=1,keepdims=True)
    loss=np.sum(-np.log(np.exp(scores[range(num_train),[y]])/np.sum(np.exp(scores),axis=1)))/num_train+reg * np.sum(np.square(W))
    exp_scores=np.exp(scores)/np.sum(np.exp(scores),axis=1,keepdims=True)
    exp_scores[range(num_train),[y]]-=1
    dW=X.T @ exp_scores/num_train+2*reg*W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW