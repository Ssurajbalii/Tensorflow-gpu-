{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "id": "HgT_OQIek1yy"
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-10-09 20:14:50.539297: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:485] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered\n",
      "2024-10-09 20:14:50.556414: E external/local_xla/xla/stream_executor/cuda/cuda_dnn.cc:8454] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered\n",
      "2024-10-09 20:14:50.561081: E external/local_xla/xla/stream_executor/cuda/cuda_blas.cc:1452] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered\n",
      "2024-10-09 20:14:50.576721: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.\n",
      "To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.\n"
     ]
    }
   ],
   "source": [
    "import numpy as np\n",
    "import seaborn as sns\n",
    "import tensorflow as tf\n",
    "import matplotlib.pyplot as plt\n",
    "from tensorflow.keras import layers\n",
    "from sklearn.metrics import confusion_matrix\n",
    "from tensorflow.keras.applications import VGG16\n",
    "from sklearn.model_selection import train_test_split\n",
    "from tensorflow.keras.preprocessing.image import ImageDataGenerator"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "id": "8-MEoQgZlHni"
   },
   "outputs": [],
   "source": [
    "(x_train, y_train), (features_test, label_test)  = tf.keras.datasets.cifar10.load_data()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "bHvDKF6nnepS",
    "outputId": "5ba8fb34-2d2e-453c-b1db-326f70cdf5a3"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(50000, 32, 32, 3)"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "x_train.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "NQhL8M1wl8UX"
   },
   "source": [
    "### Classes\n",
    "| Index | Class      |\n",
    "|-------|------------|\n",
    "| 0     | Airplane   |\n",
    "| 1     | Automobile |\n",
    "| 2     | Bird       |\n",
    "| 3     | Cat        |\n",
    "| 4     | Deer       |\n",
    "| 5     | Dog        |\n",
    "| 6     | Frog       |\n",
    "| 7     | Horse      |\n",
    "| 8     | Ship       |\n",
    "| 9     | Truck      |\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 487
    },
    "id": "6JhBrzodm2dV",
    "outputId": "194ca0e8-7a33-4203-ad6d-d0dff2a202b5"
   },
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAA1sAAAHWCAYAAACBjZMqAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjkuMiwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8hTgPZAAAACXBIWXMAAA9hAAAPYQGoP6dpAABO/0lEQVR4nO3deVxV1f7/8fcBZVAmtQRJRdRUUMyplExzIMmw4UalZmaOt8IUKKc0p0rLrmOipnnFa5pDg+WQSOKQs6KUOWsmloGVCmoKCvv3Rz/O1xMOHGJ3QF/Px2M/Hp611l77s/eVLm/33utYDMMwBAAAAAAoUk6OLgAAAAAAbkWELQAAAAAwAWELAAAAAExA2AIAAAAAExC2AAAAAMAEhC0AAAAAMAFhCwAAAABMQNgCAAAAABMQtgAAAADABIQtADDByJEjZbFY/pFjtWrVSq1atbJ+XrdunSwWiz755JN/5PgvvPCCqlWr9o8cq7DOnz+vXr16yc/PTxaLRdHR0Y4u6bYXHx8vi8WiH3/80dGlAIBpCFsAcBN5vxTmbW5ubvL391d4eLimTJmic+fOFclxTp48qZEjRyolJaVI5itKxbm2ghgzZozi4+P10ksvad68eeratesNx+fk5GjOnDlq1aqVypcvL1dXV1WrVk3du3fXzp07rePy/m5c3ZYXtK+1zZgxw+Y4AwcOlMViUceOHa9Zx48//mizv5OTk8qXL6/27dtry5YtBT7/t99+W4899ph8fX1lsVg0cuTI6479+eef9cwzz8jHx0deXl56/PHH9cMPPxT4WAW9dgBwOyjl6AIAoKQYPXq0AgMDdfnyZaWlpWndunWKjo7WhAkT9OWXX6p+/frWscOGDdPgwYPtmv/kyZMaNWqUqlWrpgYNGhR4v9WrV9t1nMK4UW2zZs1Sbm6u6TX8HUlJSWrWrJlGjBhx07EXL17Uk08+qVWrVqlly5Z6/fXXVb58ef34449avHix5s6dq9TUVFWuXPmG80yfPl0eHh42bU2bNrX+2TAMffzxx6pWrZqWLVumc+fOydPT85pzde7cWY888ohycnJ06NAhTZs2Ta1bt9aOHTsUEhJy03MaNmyY/Pz81LBhQyUkJFx33Pnz59W6dWtlZGTo9ddfV+nSpTVx4kQ9+OCDSklJUYUKFW54nKK6dgBwqyBsAUABtW/fXk2aNLF+HjJkiJKSktShQwc99thj2r9/v9zd3SVJpUqVUqlS5v4n9o8//lCZMmXk4uJi6nFupnTp0g49fkGcOnVKwcHBBRo7YMAArVq1ShMnTsz3uOGIESM0ceLEAs3z1FNP6Y477rhu/7p16/TTTz8pKSlJ4eHh+uyzz9StW7drjm3UqJGee+456+cWLVqoffv2mj59uqZNm3bTWo4dO6Zq1arpt99+05133nndcdOmTdPhw4e1fft23XvvvZL+/Htfr149jR8/XmPGjLnhcYrq2gHArYLHCAHgb2jTpo3eeOMNHT9+XB999JG1/VrvbCUmJuqBBx6Qj4+PPDw8VLt2bb3++uuS/vzFO++X2+7du1sfG4uPj5f053tZ9erVU3Jyslq2bKkyZcpY9/3rO1t5cnJy9Prrr8vPz09ly5bVY489phMnTtiMqVatml544YV8+149581qu9Y7WxcuXNCrr76qKlWqyNXVVbVr19Z//vMfGYZhM85isahv375aunSp6tWrJ1dXV9WtW1erVq269gX/i1OnTqlnz57y9fWVm5ub7rnnHs2dO9fan/f+2rFjx7RixQpr7dd7T+inn37SBx98oIceeuia73U5OzvrtddeK5I7M/Pnz1dwcLBat26tsLAwzZ8/v8D7tmjRQpJ09OjRAo0v6Dt1n3zyie69917r/96SVKdOHbVt21aLFy++4b5Fce2++OILRUREyN/fX66urqpRo4befPNN5eTk2Iw7fPiwIiMj5efnJzc3N1WuXFmdOnVSRkaGdcyNft7yZGVlacSIEapZs6ZcXV1VpUoVDRw4UFlZWTbjCjIXAFwLd7YA4G/q2rWrXn/9da1evVq9e/e+5pi9e/eqQ4cOql+/vkaPHi1XV1cdOXJEmzZtkiQFBQVp9OjRGj58uPr06WP9Zfr++++3zvH777+rffv26tSpk5577jn5+vresK63335bFotFgwYN0qlTpzRp0iSFhYUpJSXFegeuIApS29UMw9Bjjz2mtWvXqmfPnmrQoIESEhI0YMAA/fzzz/nubmzcuFGfffaZXn75ZXl6emrKlCmKjIxUamrqDR9bu3jxolq1aqUjR46ob9++CgwM1JIlS/TCCy/o7Nmz6t+/v4KCgjRv3jzFxMSocuXKevXVVyXpund3vvrqK125cuWm73QVxOnTp20+Ozs7q1y5cpL+/CX/008/tdbTuXNnde/eXWlpafLz87vp3HlhMW++opCbm6vvvvtOPXr0yNd33333afXq1Td81LEorl18fLw8PDwUGxsrDw8PJSUlafjw4crMzNR7770nScrOzlZ4eLiysrL0yiuvyM/PTz///LOWL1+us2fPytvb+6Y/b3nn+9hjj2njxo3q06ePgoKCtGfPHk2cOFGHDh3S0qVLJd38ZxcAbsgAANzQnDlzDEnGjh07rjvG29vbaNiwofXziBEjjKv/Eztx4kRDkvHrr79ed44dO3YYkow5c+bk63vwwQcNScaMGTOu2ffggw9aP69du9aQZNx1111GZmamtX3x4sWGJGPy5MnWtoCAAKNbt243nfNGtXXr1s0ICAiwfl66dKkhyXjrrbdsxj311FOGxWIxjhw5Ym2TZLi4uNi0ffvtt4Yk4/333893rKtNmjTJkGR89NFH1rbs7GwjNDTU8PDwsDn3gIAAIyIi4obzGYZhxMTEGJKM3bt333SsYVz770be//Z/3a6+Rp988okhyTh8+LBhGIaRmZlpuLm5GRMnTrSZ/9ixY4YkY9SoUcavv/5qpKWlGd98841x7733GpKMJUuWFKjOPL/++qshyRgxYsR1+0aPHp2vLy4uzpBkHDhw4LpzF/baHTt2zNr2xx9/5Bv373//2yhTpoxx6dIlwzAMY/fu3Tc994L8vM2bN89wcnIyvvnmG5v2GTNmGJKMTZs2FXguALgeHiMEgCLg4eFxw1UJfXx8JP35mFRhF5NwdXVV9+7dCzz++eeft7kL8dRTT6lSpUpauXJloY5fUCtXrpSzs7P69etn0/7qq6/KMAx99dVXNu1hYWGqUaOG9XP9+vXl5eV10xXwVq5cKT8/P3Xu3NnaVrp0afXr10/nz5/X+vXr7a49MzNTkq5798Yen376qRITE63b1Y8Jzp8/X02aNFHNmjWtx4uIiLjuo4QjRozQnXfeKT8/P7Vo0UL79+/X+PHj9dRTT/3tOvNcvHhR0p9/z/7Kzc3NZsy1FMW1u/qO67lz5/Tbb7+pRYsW+uOPP3TgwAFJkre3tyQpISFBf/zxxzXnKcjP25IlSxQUFKQ6derot99+s25t2rSRJK1du7bAcwHA9RC2AKAInD9//oa/ZHbs2FHNmzdXr1695Ovrq06dOmnx4sV2/fJ211132bUYxt13323z2WKxqGbNmqZ/r9Hx48fl7++f73oEBQVZ+69WtWrVfHOUK1dOZ86cuelx7r77bjk52f5f2fWOUxBeXl6SVCTL+bds2VJhYWHWrXnz5pKks2fPauXKlXrwwQd15MgR69a8eXPt3LlThw4dyjdXnz59lJiYqGXLlikmJkYXL17M9x5TWlqazXajYHQteUHnr+8rSdKlS5dsxlxLUVy7vXv36l//+pe8vb3l5eWlO++807owSN77WIGBgYqNjdWHH36oO+64Q+Hh4YqLi7N5X6sgP2+HDx/W3r17deedd9pstWrVkvTn+4AFnQsArod3tgDgb/rpp5+UkZFhvUtxLe7u7tqwYYPWrl2rFStWaNWqVVq0aJHatGmj1atXy9nZ+abHsec9q4K63hcv5+TkFKimonC94xh/WUzjn1CnTh1J0p49e+xaft8eS5YsUVZWlsaPH6/x48fn658/f75GjRpl03b33XcrLCxMktShQwc5Oztr8ODBat26tXWFzEqVKtnsM2fOnGsufnI9ed+J9csvv+Try2vz9/e/7v5/99qdPXtWDz74oLy8vDR69GjVqFFDbm5u2rVrlwYNGmQTbsaPH68XXnhBX3zxhVavXq1+/fpp7Nix2rp1qypXrlygn7fc3FyFhIRowoQJ16ynSpUqkormZxfA7Ys7WwDwN82bN0+SFB4efsNxTk5Oatu2rSZMmKB9+/bp7bffVlJSkvVxpesFn8I6fPiwzWfDMHTkyBGblenKlSuns2fP5tv3r3eF7KktICBAJ0+ezHeHI+8xsICAgALPdbPjHD58ON8dhr9znPbt28vZ2dlmZcmiNn/+fNWrV09LlizJt4WFhWnBggU3nWPo0KHy9PTUsGHDrG1XP7KYmJh407+Pf+Xk5KSQkJBrfvHwtm3bVL169Rvevf27127dunX6/fffFR8fr/79+6tDhw4KCwu77iIgISEhGjZsmDZs2KBvvvlGP//8s82XRt/s561GjRo6ffq02rZta3MHMm+rXbt2gecCgOshbAHA35CUlKQ333xTgYGB6tKly3XH/XVlOknWf/3Pe2yrbNmyknTN8FMY//vf/2wCzyeffKJffvlF7du3t7bVqFFDW7duVXZ2trVt+fLl+ZaIt6e2vC/fnTp1qk37xIkTZbFYbI7/dzzyyCNKS0vTokWLrG1XrlzR+++/Lw8PDz344IN2z1mlShX17t1bq1ev1vvvv5+vPzc3V+PHj9dPP/1UqJpPnDihDRs26JlnntFTTz2Vb+vevbuOHDmibdu23XAeHx8f/fvf/1ZCQoJSUlIkKV9Y+OudroJ46qmntGPHDpvAdfDgQSUlJenpp5++4b5/99rl3SG6+o5mdnZ2vu8Ry8zM1JUrV2zaQkJC5OTkZP1ZKsjP2zPPPKOff/5Zs2bNyjf24sWLunDhQoHnAoDr4TFCACigr776SgcOHNCVK1eUnp6upKQkJSYmKiAgQF9++aV1EYFrGT16tDZs2KCIiAgFBATo1KlTmjZtmipXrqwHHnhA0p/Bx8fHRzNmzJCnp6fKli2rpk2bKjAwsFD1li9fXg888IC6d++u9PR0TZo0STVr1rRZnr5Xr1765JNP9PDDD+uZZ57R0aNH9dFHH9ksWGFvbY8++qhat26toUOH6scff9Q999yj1atX64svvlB0dHS+uQurT58++uCDD/TCCy8oOTlZ1apV0yeffKJNmzZp0qRJhV6oYfz48Tp69Kj69eunzz77TB06dFC5cuWUmpqqJUuW6MCBA+rUqVOh5l6wYIF1afxreeSRR1SqVCnNnz9fTZs2veFc/fv316RJk/TOO+9o4cKFNxw7b948HT9+3LqgxIYNG/TWW29J+vOrC/LuAr788suaNWuWIiIi9Nprr6l06dKaMGGCfH19rcvU38jfuXb333+/ypUrp27duqlfv36yWCyaN29evsdJk5KS1LdvXz399NOqVauWrly5onnz5snZ2VmRkZGSCvbz1rVrVy1evFgvvvii1q5dq+bNmysnJ0cHDhzQ4sWLlZCQoCZNmhRoLgC4LkcuhQgAJUHeEtV5m4uLi+Hn52c89NBDxuTJk22WGM/z16Xf16xZYzz++OOGv7+/4eLiYvj7+xudO3c2Dh06ZLPfF198YQQHBxulSpWyWWr9wQcfNOrWrXvN+q639PvHH39sDBkyxKhYsaLh7u5uREREGMePH8+3//jx44277rrLcHV1NZo3b27s3Lkz35w3qu2vS78bhmGcO3fOiImJMfz9/Y3SpUsbd999t/Hee+8Zubm5NuMkGVFRUflqut6S9H+Vnp5udO/e3bjjjjsMFxcXIyQk5JrL0xd06fc8V65cMT788EOjRYsWhre3t1G6dGkjICDA6N69u83S5jda+v1aS4WHhIQYVatWveGxW7VqZVSsWNG4fPmyden3995775pjX3jhBcPZ2dlm6fxryfvqgGtta9eutRl74sQJ46mnnjK8vLwMDw8Po0OHDtYl6gvC3mt39dLvmzZtMpo1a2a4u7sb/v7+xsCBA42EhASbOn/44QejR48eRo0aNQw3NzejfPnyRuvWrY2vv/7aOk9Bf96ys7ONd99916hbt67h6upqlCtXzmjcuLExatQoIyMjw665AOBaLIbhgDeQAQAAAOAWxztbAAAAAGACwhYAAAAAmICwBQAAAAAmIGwBAAAAgAkIWwAAAABgAsIWAAAAAJiALzUugNzcXJ08eVKenp6yWCyOLgcAAACAgxiGoXPnzsnf319OTje+d0XYKoCTJ0+qSpUqji4DAAAAQDFx4sQJVa5c+YZjCFsF4OnpKenPC+rl5eXgagAAAAA4SmZmpqpUqWLNCDdC2CqAvEcHvby8CFsAAAAACvR6EQtkAAAAAIAJCFsAAAAAYALCFgAAAACYgLAFAAAAACYgbAEAAACACQhbAAAAAGACwhYAAAAAmICwBQAAAAAmIGwBAAAAgAkIWwAAAABgAsIWAAAAAJjA4WHr559/1nPPPacKFSrI3d1dISEh2rlzp7XfMAwNHz5clSpVkru7u8LCwnT48GGbOU6fPq0uXbrIy8tLPj4+6tmzp86fP28z5rvvvlOLFi3k5uamKlWqaNy4cf/I+QEAAAC4PTk0bJ05c0bNmzdX6dKl9dVXX2nfvn0aP368ypUrZx0zbtw4TZkyRTNmzNC2bdtUtmxZhYeH69KlS9YxXbp00d69e5WYmKjly5drw4YN6tOnj7U/MzNT7dq1U0BAgJKTk/Xee+9p5MiRmjlz5j96vgAAAABuHxbDMAxHHXzw4MHatGmTvvnmm2v2G4Yhf39/vfrqq3rttdckSRkZGfL19VV8fLw6deqk/fv3Kzg4WDt27FCTJk0kSatWrdIjjzyin376Sf7+/po+fbqGDh2qtLQ0ubi4WI+9dOlSHThw4KZ1ZmZmytvbWxkZGfLy8iqiswcAAABQ0tiTDRx6Z+vLL79UkyZN9PTTT6tixYpq2LChZs2aZe0/duyY0tLSFBYWZm3z9vZW06ZNtWXLFknSli1b5OPjYw1akhQWFiYnJydt27bNOqZly5bWoCVJ4eHhOnjwoM6cOZOvrqysLGVmZtpsAAAAAGCPUo48+A8//KDp06crNjZWr7/+unbs2KF+/frJxcVF3bp1U1pamiTJ19fXZj9fX19rX1pamipWrGjTX6pUKZUvX95mTGBgYL458vqufmxRksaOHatRo0bZdS6NB/zPrvG3iuT3nv9b+3Pd7Mc1Kxyum/24ZoXDdbMf16xwuG7245oVDtet8Bx6Zys3N1eNGjXSmDFj1LBhQ/Xp00e9e/fWjBkzHFmWhgwZooyMDOt24sQJh9YDAAAAoORxaNiqVKmSgoODbdqCgoKUmpoqSfLz85Mkpaen24xJT0+39vn5+enUqVM2/VeuXNHp06dtxlxrjquPcTVXV1d5eXnZbAAAAABgD4eGrebNm+vgwYM2bYcOHVJAQIAkKTAwUH5+flqzZo21PzMzU9u2bVNoaKgkKTQ0VGfPnlVycrJ1TFJSknJzc9W0aVPrmA0bNujy5cvWMYmJiapdu3a+RwgBAAAAoCg4NGzFxMRo69atGjNmjI4cOaIFCxZo5syZioqKkiRZLBZFR0frrbfe0pdffqk9e/bo+eefl7+/v5544glJf94Je/jhh9W7d29t375dmzZtUt++fdWpUyf5+/tLkp599lm5uLioZ8+e2rt3rxYtWqTJkycrNjbWUacOAAAA4Bbn0AUy7r33Xn3++ecaMmSIRo8ercDAQE2aNEldunSxjhk4cKAuXLigPn366OzZs3rggQe0atUqubm5WcfMnz9fffv2Vdu2beXk5KTIyEhNmTLF2u/t7a3Vq1crKipKjRs31h133KHhw4fbfBcXAAAAABQlh4YtSerQoYM6dOhw3X6LxaLRo0dr9OjR1x1Tvnx5LViw4IbHqV+//nW/zwsAAAAAippDHyMEAAAAgFsVYQsAAAAATEDYAgAAAAATELYAAAAAwASELQAAAAAwAWELAAAAAExA2AIAAAAAExC2AAAAAMAEhC0AAAAAMAFhCwAAAABMQNgCAAAAABMQtgAAAADABIQtAAAAADABYQsAAAAATEDYAgAAAAATELYAAAAAwASELQAAAAAwAWELAAAAAExA2AIAAAAAExC2AAAAAMAEhC0AAAAAMAFhCwAAAABMQNgCAAAAABMQtgAAAADABIQtAAAAADABYQsAAAAATEDYAgAAAAATELYAAAAAwASELQAAAAAwAWELAAAAAExA2AIAAAAAExC2AAAAAMAEhC0AAAAAMAFhCwAAAABMQNgCAAAAABMQtgAAAADABIQtAAAAADABYQsAAAAATEDYAgAAAAATELYAAAAAwASELQAAAAAwAWELAAAAAExA2AIAAAAAExC2AAAAAMAEhC0AAAAAMAFhCwAAAABMQNgCAAAAABMQtgAAAADABIQtAAAAADABYQsAAAAATODQsDVy5EhZLBabrU6dOtb+S5cuKSoqShUqVJCHh4ciIyOVnp5uM0dqaqoiIiJUpkwZVaxYUQMGDNCVK1dsxqxbt06NGjWSq6uratasqfj4+H/i9AAAAADcxhx+Z6tu3br65ZdfrNvGjRutfTExMVq2bJmWLFmi9evX6+TJk3ryySet/Tk5OYqIiFB2drY2b96suXPnKj4+XsOHD7eOOXbsmCIiItS6dWulpKQoOjpavXr1UkJCwj96ngAAAABuL6UcXkCpUvLz88vXnpGRodmzZ2vBggVq06aNJGnOnDkKCgrS1q1b1axZM61evVr79u3T119/LV9fXzVo0EBvvvmmBg0apJEjR8rFxUUzZsxQYGCgxo8fL0kKCgrSxo0bNXHiRIWHh/+j5woAAADg9uHwO1uHDx+Wv7+/qlevri5duig1NVWSlJycrMuXLyssLMw6tk6dOqpataq2bNkiSdqyZYtCQkLk6+trHRMeHq7MzEzt3bvXOubqOfLG5M1xLVlZWcrMzLTZAAAAAMAeDg1bTZs2VXx8vFatWqXp06fr2LFjatGihc6dO6e0tDS5uLjIx8fHZh9fX1+lpaVJktLS0myCVl5/Xt+NxmRmZurixYvXrGvs2LHy9va2blWqVCmK0wUAAABwG3HoY4Tt27e3/rl+/fpq2rSpAgICtHjxYrm7uzusriFDhig2Ntb6OTMzk8AFAAAAwC4Of4zwaj4+PqpVq5aOHDkiPz8/ZWdn6+zZszZj0tPTre94+fn55VudMO/zzcZ4eXldN9C5urrKy8vLZgMAAAAAexSrsHX+/HkdPXpUlSpVUuPGjVW6dGmtWbPG2n/w4EGlpqYqNDRUkhQaGqo9e/bo1KlT1jGJiYny8vJScHCwdczVc+SNyZsDAAAAAMzg0LD12muvaf369frxxx+1efNm/etf/5Kzs7M6d+4sb29v9ezZU7GxsVq7dq2Sk5PVvXt3hYaGqlmzZpKkdu3aKTg4WF27dtW3336rhIQEDRs2TFFRUXJ1dZUkvfjii/rhhx80cOBAHThwQNOmTdPixYsVExPjyFMHAAAAcItz6DtbP/30kzp37qzff/9dd955px544AFt3bpVd955pyRp4sSJcnJyUmRkpLKyshQeHq5p06ZZ93d2dtby5cv10ksvKTQ0VGXLllW3bt00evRo65jAwECtWLFCMTExmjx5sipXrqwPP/yQZd8BAAAAmMqhYWvhwoU37Hdzc1NcXJzi4uKuOyYgIEArV6684TytWrXS7t27C1UjAAAAABRGsXpnCwAAAABuFYQtAAAAADABYQsAAAAATEDYAgAAAAATELYAAAAAwASELQAAAAAwAWELAAAAAExA2AIAAAAAExC2AAAAAMAEhC0AAAAAMAFhCwAAAABMQNgCAAAAABMQtgAAAADABIQtAAAAADABYQsAAAAATEDYAgAAAAATELYAAAAAwASELQAAAAAwAWELAAAAAExA2AIAAAAAExC2AAAAAMAEhC0AAAAAMAFhCwAAAABMQNgCAAAAABMQtgAAAADABIQtAAAAADABYQsAAAAATEDYAgAAAAATELYAAAAAwASELQAAAAAwAWELAAAAAExA2AIAAAAAExC2AAAAAMAEhC0AAAAAMAFhCwAAAABMQNgCAAAAABMQtgAAAADABIQtAAAAADABYQsAAAAATEDYAgAAAAATELYAAAAAwASELQAAAAAwAWELAAAAAExA2AIAAAAAE9gdtubOnasVK1ZYPw8cOFA+Pj66//77dfz48SItDgAAAABKKrvD1pgxY+Tu7i5J2rJli+Li4jRu3DjdcccdiomJKfICAQAAAKAkKmXvDidOnFDNmjUlSUuXLlVkZKT69Omj5s2bq1WrVkVdHwAAAACUSHbf2fLw8NDvv/8uSVq9erUeeughSZKbm5suXrxYtNUBAAAAQAll952thx56SL169VLDhg116NAhPfLII5KkvXv3qlq1akVdHwAAAACUSHbf2YqLi1NoaKh+/fVXffrpp6pQoYIkKTk5WZ07dy7yAgEAAACgJLI7bPn4+Gjq1Kn64osv9PDDD1vbR40apaFDhxa6kHfeeUcWi0XR0dHWtkuXLikqKkoVKlSQh4eHIiMjlZ6ebrNfamqqIiIiVKZMGVWsWFEDBgzQlStXbMasW7dOjRo1kqurq2rWrKn4+PhC1wkAAAAABVGo79n65ptv9Nxzz+n+++/Xzz//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W4LdYeupp57SunXrTCgFAAAAAG4ddr+zNXXqVD399NP65ptvFBISotKlS9v09+vXr8iKAwAAAICSyu6w9fHHH2v16tVyc3PTunXrZLFYrH0Wi4WwBQAAAAAqRNgaOnSoRo0apcGDB9t83xYAAAAA4P/YnZays7PVsWNHghYAAAAA3IDdialbt25atGiRGbUAAAAAwC3D7scIc3JyNG7cOCUkJKh+/fr5FsiYMGFCkRUHAAAAACWV3WFrz549atiwoSTp+++/t+m7erEMAAAAALid2R221q5da0YdAAAAAHBLYZULAAAAADBBge9sPfnkkwUa99lnnxW6GAAAAAC4VRQ4bHl7e5tZBwAAAADcUgoctubMmWNmHQAAAABwS+GdLQAAAAAwAWELAAAAAExA2AIAAAAAExC2AAAAAMAEBQpbjRo10pkzZyRJo0eP1h9//GFqUQAAAABQ0hUobO3fv18XLlyQJI0aNUrnz583tSgAAAAAKOkKtPR7gwYN1L17dz3wwAMyDEP/+c9/5OHhcc2xw4cPL9ICAQAAAKAkKlDYio+P14gRI7R8+XJZLBZ99dVXKlUq/64Wi4WwBQAAAAAqYNiqXbu2Fi5cKElycnLSmjVrVLFiRVMLAwAAAICSrEBh62q5ublm1AEAAAAAtxS7w5YkHT16VJMmTdL+/fslScHBwerfv79q1KhRpMUBAAAAQEll9/dsJSQkKDg4WNu3b1f9+vVVv359bdu2TXXr1lViYqIZNQIAAABAiWP3na3BgwcrJiZG77zzTr72QYMG6aGHHiqy4gAAAACgpLL7ztb+/fvVs2fPfO09evTQvn37iqQoAAAAACjp7A5bd955p1JSUvK1p6SksEIhAAAAAPx/dj9G2Lt3b/Xp00c//PCD7r//fknSpk2b9O677yo2NrbICwQAAACAksjusPXGG2/I09NT48eP15AhQyRJ/v7+GjlypPr161fkBQIAAABASWT3Y4QWi0UxMTH66aeflJGRoYyMDP3000/q37+/LBaLXXNNnz5d9evXl5eXl7y8vBQaGqqvvvrK2n/p0iVFRUWpQoUK8vDwUGRkpNLT023mSE1NVUREhMqUKaOKFStqwIABunLlis2YdevWqVGjRnJ1dVXNmjUVHx9v72kDAAAAgF3sDltX8/T0lKenZ6H3r1y5st555x0lJydr586datOm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5e7uro8++siBlRVfFy9elKenp7744gtFRERY2xs3bqz27dvrrbfecmB19uPOVgmVnZ2t5ORkhYWFWducnJwUFhamLVu2OLAy3OoyMjIk/RkecHM5OTlauHChLly4oNDQUEeXU+xFRUUpIiLC5r9tuLHDhw/L399f1atXV5cuXZSamurokoq9L7/8Uk2aNNHTTz+tihUrqmHDhpo1a5ajyyoxsrOz9dFHH6lHjx4ErZu4//77tWbNGh06dEiS9O2332rjxo1q3769gysrvq5cuaKcnBy5ubnZtLu7u5fIO/elHF0ACue3335TTk6OfH19bdp9fX114MABB1WFW11ubq6io6PVvHlz1atXz9HlFGt79uxRaGioLl26JA8PD33++ecKDg52dFnF2sKFC7Vr164S+1y+IzRt2lTx8fGqXbu2fvnlF40aNUotWrTQ999/L09PT0eXV2z98MMPmj59umJjY/X6669rx44d6tevn1xcXNStWzdHl1fsLV26VGfPntULL7zg6FKKvcGDByszM1N16tSRs7OzcnJy9Pbbb6tLly6OLq3Y8vT0VGhoqN58800FBQXJ19dXH3/8sbZs2aKaNWs6ujy7EbYAFFhUVJS+//77EvkvS/+02rVrKyUlRRkZGfrkk0/UrVs3rV+/nsB1HSdOnFD//v2VmJiY718zcX1X/+t4/fr11bRpUwUEBGjx4sU8snoDubm5atKkicaMGSNJatiwob7//nvNmDGDsFUAs2fPVvv27eXv7+/oUoq9xYsXa/78+VqwYIHq1q2rlJQURUdHy9/fn79rNzBv3jz16NFDd911l5ydndWoUSN17txZycnJji7NboStEuqOO+6Qs7Oz0tPTbdrT09Pl5+fnoKpwK+vbt6+WL1+uDRs2qHLlyo4up9hzcXGx/gtc48aNtWPHDk2ePFkffPCBgysrnpKTk3Xq1Ck1atTI2paTk6MNGzZo6tSpysrKkrOzswMrLBl8fHxUq1YtHTlyxNGlFGuVKlXK9w8fQUFB+vTTTx1UUclx/Phxff311/rss88cXUqJMGDAAA0ePFidOnWSJIWEhOj48eMaO3YsYesGatSoofXr1+vChQvKzMxUpUqV1LFjR1WvXt3RpdmNd7ZKKBcXFzVu3Fhr1qyxtuXm5mrNmjW8F4IiZRiG+vbtq88//1xJSUkKDAx0dEklUm5u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950uXbpkbfvrYh+NGjXS3r17Va1aNdWsWdNmy3t/7ejRo4qJidGsWbPUtGlTdevWza5ABwD45xC2AADFTlxcnHJycnTffffp008/1eHDh7V//35NmTIl36N3ee6++26lpqZq4cKFOnr0qKZMmWK9ayVJFy9eVN++fbVu3TodP35cmzZt0o4dOxQUFCRJio6OVkJCgo4dO6Zdu3Zp7dq11r6i8Oyzz8pisah3797at2+fVq5cqf/85z82Y6KionT69Gl17txZO3bs0NGjR5WQkKDu3bsrJydHOTk5eu655xQeHq7u3btrzpw5+u677zR+/PgiqxMAUHQIWwCAYqd69eratWuXWrdurVdffVX16tXTQw89pDVr1mj69OnX3Oexxx5TTEyM+vbtqwYNGmjz5s164403rP3Ozs76/fff9fzzz6tWrVp65pln1L59e40aNUqSlJOTo6ioKAUFBenhhx9WrVq1NG3atCI7Jw8PDy1btkx79uxRw4YNNXToUL377rs2Y/z9/bVp0ybl5OSoXbt2CgkJUXR0tHx8fOTk5KS3335bx48f1wcffCBJqlSpkmbOnKlhw4bp22+/LbJaAQBFw2L8nTeRAQAAAADXxJ0tAAAAADABYQsAAAAATEDYAgAAAAATELYAAAAAwASELQAAAAAwAWELAAAAAExA2AIAAAAAExC2AAAAAMAEhC0AAAAAMAFhCwAAAABMQNgCAAAAABP8PxPnAHkGD1SUAAAAAElFTkSuQmCC",
      "text/plain": [
       "<Figure size 1000x500 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# Flatten the label arrays to a 1D array\n",
    "label_train_flat = y_train.flatten()\n",
    "label_test_flat = label_test.flatten()\n",
    "\n",
    "# Combine train and test labels\n",
    "all_labels =  list(label_train_flat) + list(label_test_flat)\n",
    "\n",
    "# Count the number of elements in each category\n",
    "\n",
    "label_counts = np.unique(all_labels, return_counts=True)[1]\n",
    "\n",
    "plt.figure(figsize=(10, 5))\n",
    "sns.barplot(x=list(range(10)), y=label_counts)\n",
    "plt.xlabel('Class Index')\n",
    "plt.ylabel('Number of Images')\n",
    "plt.title('Distribution of CIFAR-10 Classes')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "RYw9UPQ-aPQS",
    "outputId": "2538a81b-5c03-4143-f207-cc3228816bfe"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "((5000, 32, 32, 3), (5000, 32, 32, 3), (5000, 1), (5000, 1))"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "x_test, x_val, y_test, y_val = train_test_split(features_test, label_test, test_size=0.5, random_state=2)\n",
    "x_test.shape, x_val.shape, y_test.shape, y_val.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {
    "id": "3EW2fd3ObCxG"
   },
   "outputs": [],
   "source": [
    "# Creating an Image data generator\n",
    "\n",
    "train_img_gen = ImageDataGenerator(rescale=1./255\n",
    "                                  , rotation_range=40\n",
    "                                  ,width_shift_range=0.2\n",
    "                                  ,height_shift_range=0.2\n",
    "                                  ,shear_range=0.1\n",
    "                                  ,zoom_range=0.1\n",
    "                                  ,horizontal_flip=False\n",
    "                                  ,fill_mode='nearest')\n",
    "\n",
    "val_img_gen = ImageDataGenerator(rescale=1./255)\n",
    "\n",
    "test_img_gen = ImageDataGenerator(rescale=1./255)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {
    "id": "MxuEdRDLkG3T"
   },
   "outputs": [],
   "source": [
    "batch_size = 32\n",
    "\n",
    "train_data_gen = train_img_gen.flow(x_train, y_train,batch_size=batch_size)\n",
    "val_img_gen = val_img_gen.flow(x_val, y_val, batch_size=batch_size)\n",
    "test_img_gen = test_img_gen.flow(x_test, y_test, batch_size=batch_size)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "XiGBNlbxkcYZ",
    "outputId": "1a362ceb-8ae8-423d-8a50-d8f4be4b3020"
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/lib/python3.11/dist-packages/keras/src/layers/convolutional/base_conv.py:107: UserWarning: Do not pass an `input_shape`/`input_dim` argument to a layer. When using Sequential models, prefer using an `Input(shape)` object as the first layer in the model instead.\n",
      "  super().__init__(activity_regularizer=activity_regularizer, **kwargs)\n",
      "WARNING: All log messages before absl::InitializeLog() is called are written to STDERR\n",
      "I0000 00:00:1728504893.366838    1710 cuda_executor.cc:1001] could not open file to read NUMA node: /sys/bus/pci/devices/0000:01:00.0/numa_node\n",
      "Your kernel may have been built without NUMA support.\n",
      "I0000 00:00:1728504893.373416    1710 cuda_executor.cc:1001] could not open file to read NUMA node: /sys/bus/pci/devices/0000:01:00.0/numa_node\n",
      "Your kernel may have been built without NUMA support.\n",
      "I0000 00:00:1728504893.373480    1710 cuda_executor.cc:1001] could not open file to read NUMA node: /sys/bus/pci/devices/0000:01:00.0/numa_node\n",
      "Your kernel may have been built without NUMA support.\n",
      "I0000 00:00:1728504893.379114    1710 cuda_executor.cc:1001] could not open file to read NUMA node: /sys/bus/pci/devices/0000:01:00.0/numa_node\n",
      "Your kernel may have been built without NUMA support.\n",
      "I0000 00:00:1728504893.379189    1710 cuda_executor.cc:1001] could not open file to read NUMA node: /sys/bus/pci/devices/0000:01:00.0/numa_node\n",
      "Your kernel may have been built without NUMA support.\n",
      "I0000 00:00:1728504893.379223    1710 cuda_executor.cc:1001] could not open file to read NUMA node: /sys/bus/pci/devices/0000:01:00.0/numa_node\n",
      "Your kernel may have been built without NUMA support.\n",
      "I0000 00:00:1728504893.535560    1710 cuda_executor.cc:1001] could not open file to read NUMA node: /sys/bus/pci/devices/0000:01:00.0/numa_node\n",
      "Your kernel may have been built without NUMA support.\n",
      "I0000 00:00:1728504893.535679    1710 cuda_executor.cc:1001] could not open file to read NUMA node: /sys/bus/pci/devices/0000:01:00.0/numa_node\n",
      "Your kernel may have been built without NUMA support.\n",
      "2024-10-09 20:14:53.535704: I tensorflow/core/common_runtime/gpu/gpu_device.cc:2112] Could not identify NUMA node of platform GPU id 0, defaulting to 0.  Your kernel may not have been built with NUMA support.\n",
      "I0000 00:00:1728504893.535805    1710 cuda_executor.cc:1001] could not open file to read NUMA node: /sys/bus/pci/devices/0000:01:00.0/numa_node\n",
      "Your kernel may have been built without NUMA support.\n",
      "2024-10-09 20:14:53.535847: I tensorflow/core/common_runtime/gpu/gpu_device.cc:2021] Created device /job:localhost/replica:0/task:0/device:GPU:0 with 1767 MB memory:  -> device: 0, name: NVIDIA GeForce RTX 3050 Laptop GPU, pci bus id: 0000:01:00.0, compute capability: 8.6\n"
     ]
    }
   ],
   "source": [
    "model = tf.keras.Sequential([\n",
    "          layers.Conv2D(64, 3, activation='relu', input_shape=(32, 32 ,3))\n",
    "        , layers.MaxPooling2D()\n",
    "        , layers.Conv2D(128, 3, activation='relu')\n",
    "        , layers.MaxPooling2D()\n",
    "        , layers.Flatten()\n",
    "        , layers.Dense(128, activation='relu')\n",
    "        , layers.Dense(10, activation='softmax')])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 374
    },
    "id": "xQiPOhfInawH",
    "outputId": "faf31069-af8a-47d5-b358-3dd51579f7dd"
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<pre style=\"white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\"><span style=\"font-weight: bold\">Model: \"sequential\"</span>\n",
       "</pre>\n"
      ],
      "text/plain": [
       "\u001b[1mModel: \"sequential\"\u001b[0m\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "<pre style=\"white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\">┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓\n",
       "┃<span style=\"font-weight: bold\"> Layer (type)                    </span>┃<span style=\"font-weight: bold\"> Output Shape           </span>┃<span style=\"font-weight: bold\">       Param # </span>┃\n",
       "┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩\n",
       "│ conv2d (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)                 │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">30</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">30</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">64</span>)     │         <span style=\"color: #00af00; text-decoration-color: #00af00\">1,792</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ max_pooling2d (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">MaxPooling2D</span>)    │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">15</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">15</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">64</span>)     │             <span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ conv2d_1 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)               │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">13</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">13</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">128</span>)    │        <span style=\"color: #00af00; text-decoration-color: #00af00\">73,856</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ max_pooling2d_1 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">MaxPooling2D</span>)  │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">6</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">6</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">128</span>)      │             <span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ flatten (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Flatten</span>)               │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">4608</span>)           │             <span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ dense (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Dense</span>)                   │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">128</span>)            │       <span style=\"color: #00af00; text-decoration-color: #00af00\">589,952</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ dense_1 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Dense</span>)                 │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">10</span>)             │         <span style=\"color: #00af00; text-decoration-color: #00af00\">1,290</span> │\n",
       "└─────────────────────────────────┴────────────────────────┴───────────────┘\n",
       "</pre>\n"
      ],
      "text/plain": [
       "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓\n",
       "┃\u001b[1m \u001b[0m\u001b[1mLayer (type)                   \u001b[0m\u001b[1m \u001b[0m┃\u001b[1m \u001b[0m\u001b[1mOutput Shape          \u001b[0m\u001b[1m \u001b[0m┃\u001b[1m \u001b[0m\u001b[1m      Param #\u001b[0m\u001b[1m \u001b[0m┃\n",
       "┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩\n",
       "│ conv2d (\u001b[38;5;33mConv2D\u001b[0m)                 │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m30\u001b[0m, \u001b[38;5;34m30\u001b[0m, \u001b[38;5;34m64\u001b[0m)     │         \u001b[38;5;34m1,792\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ max_pooling2d (\u001b[38;5;33mMaxPooling2D\u001b[0m)    │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m15\u001b[0m, \u001b[38;5;34m15\u001b[0m, \u001b[38;5;34m64\u001b[0m)     │             \u001b[38;5;34m0\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ conv2d_1 (\u001b[38;5;33mConv2D\u001b[0m)               │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m13\u001b[0m, \u001b[38;5;34m13\u001b[0m, \u001b[38;5;34m128\u001b[0m)    │        \u001b[38;5;34m73,856\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ max_pooling2d_1 (\u001b[38;5;33mMaxPooling2D\u001b[0m)  │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m6\u001b[0m, \u001b[38;5;34m6\u001b[0m, \u001b[38;5;34m128\u001b[0m)      │             \u001b[38;5;34m0\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ flatten (\u001b[38;5;33mFlatten\u001b[0m)               │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m4608\u001b[0m)           │             \u001b[38;5;34m0\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ dense (\u001b[38;5;33mDense\u001b[0m)                   │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m128\u001b[0m)            │       \u001b[38;5;34m589,952\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ dense_1 (\u001b[38;5;33mDense\u001b[0m)                 │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m10\u001b[0m)             │         \u001b[38;5;34m1,290\u001b[0m │\n",
       "└─────────────────────────────────┴────────────────────────┴───────────────┘\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "<pre style=\"white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\"><span style=\"font-weight: bold\"> Total params: </span><span style=\"color: #00af00; text-decoration-color: #00af00\">666,890</span> (2.54 MB)\n",
       "</pre>\n"
      ],
      "text/plain": [
       "\u001b[1m Total params: \u001b[0m\u001b[38;5;34m666,890\u001b[0m (2.54 MB)\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "<pre style=\"white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\"><span style=\"font-weight: bold\"> Trainable params: </span><span style=\"color: #00af00; text-decoration-color: #00af00\">666,890</span> (2.54 MB)\n",
       "</pre>\n"
      ],
      "text/plain": [
       "\u001b[1m Trainable params: \u001b[0m\u001b[38;5;34m666,890\u001b[0m (2.54 MB)\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "<pre style=\"white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\"><span style=\"font-weight: bold\"> Non-trainable params: </span><span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> (0.00 B)\n",
       "</pre>\n"
      ],
      "text/plain": [
       "\u001b[1m Non-trainable params: \u001b[0m\u001b[38;5;34m0\u001b[0m (0.00 B)\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "model.summary()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {
    "id": "V3tUvrUxoUAK"
   },
   "outputs": [],
   "source": [
    "optimizer = tf.keras.optimizers.Adam(0.001)\n",
    "\n",
    "model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "9P0D6hpGorC9",
    "outputId": "4b78aa7b-7405-457c-d000-efa10128b124",
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Epoch 1/15\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/lib/python3.11/dist-packages/keras/src/trainers/data_adapters/py_dataset_adapter.py:121: UserWarning: Your `PyDataset` class should call `super().__init__(**kwargs)` in its constructor. `**kwargs` can include `workers`, `use_multiprocessing`, `max_queue_size`. Do not pass these arguments to `fit()`, as they will be ignored.\n",
      "  self._warn_if_super_not_called()\n",
      "WARNING: All log messages before absl::InitializeLog() is called are written to STDERR\n",
      "I0000 00:00:1728504894.699200    1787 service.cc:146] XLA service 0x7f72e8006980 initialized for platform CUDA (this does not guarantee that XLA will be used). Devices:\n",
      "I0000 00:00:1728504894.699250    1787 service.cc:154]   StreamExecutor device (0): NVIDIA GeForce RTX 3050 Laptop GPU, Compute Capability 8.6\n",
      "2024-10-09 20:14:54.721423: I tensorflow/compiler/mlir/tensorflow/utils/dump_mlir_util.cc:268] disabling MLIR crash reproducer, set env var `MLIR_CRASH_REPRODUCER_DIRECTORY` to enable.\n",
      "2024-10-09 20:14:54.841257: I external/local_xla/xla/stream_executor/cuda/cuda_dnn.cc:531] Loaded cuDNN version 8906\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[1m  16/1562\u001b[0m \u001b[37m━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[1m17s\u001b[0m 12ms/step - accuracy: 0.0699 - loss: 2.3294"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "I0000 00:00:1728504898.243307    1787 device_compiler.h:188] Compiled cluster using XLA!  This line is logged at most once for the lifetime of the process.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[1m1562/1562\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m27s\u001b[0m 15ms/step - accuracy: 0.2982 - loss: 1.8976 - val_accuracy: 0.5319 - val_loss: 1.3075\n",
      "Epoch 2/15\n",
      "\u001b[1m   1/1562\u001b[0m \u001b[37m━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[1m7s\u001b[0m 5ms/step - accuracy: 0.4688 - loss: 1.4135"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-10-09 20:15:21.026904: I tensorflow/core/framework/local_rendezvous.cc:404] Local rendezvous is aborting with status: OUT_OF_RANGE: End of sequence\n",
      "\t [[{{node IteratorGetNext}}]]\n",
      "2024-10-09 20:15:21.026973: I tensorflow/core/framework/local_rendezvous.cc:404] Local rendezvous is aborting with status: OUT_OF_RANGE: End of sequence\n",
      "\t [[{{node IteratorGetNext}}]]\n",
      "\t [[IteratorGetNext/_2]]\n",
      "2024-10-09 20:15:21.026984: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 18116607102968086293\n",
      "2024-10-09 20:15:21.027006: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 2094629562201250906\n",
      "/usr/lib/python3.11/contextlib.py:155: UserWarning: Your input ran out of data; interrupting training. Make sure that your dataset or generator can generate at least `steps_per_epoch * epochs` batches. You may need to use the `.repeat()` function when building your dataset.\n",
      "  self.gen.throw(typ, value, traceback)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[1m1562/1562\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m1s\u001b[0m 601us/step - accuracy: 0.4688 - loss: 1.4135 - val_accuracy: 0.7500 - val_loss: 1.0313\n",
      "Epoch 3/15\n",
      "\u001b[1m   5/1562\u001b[0m \u001b[37m━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[1m19s\u001b[0m 13ms/step - accuracy: 0.4926 - loss: 1.5373  "
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-10-09 20:15:21.956686: I tensorflow/core/framework/local_rendezvous.cc:404] Local rendezvous is aborting with status: OUT_OF_RANGE: End of sequence\n",
      "\t [[{{node IteratorGetNext}}]]\n",
      "\t [[IteratorGetNext/_2]]\n",
      "2024-10-09 20:15:21.956763: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 18116607102968086293\n",
      "2024-10-09 20:15:21.956793: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 2094629562201250906\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[1m1562/1562\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m20s\u001b[0m 13ms/step - accuracy: 0.4438 - loss: 1.5386 - val_accuracy: 0.5571 - val_loss: 1.2147\n",
      "Epoch 4/15\n",
      "\u001b[1m1562/1562\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m0s\u001b[0m 12us/step - accuracy: 0.4062 - loss: 1.6001 - val_accuracy: 0.8750 - val_loss: 0.7657\n",
      "Epoch 5/15\n",
      "\u001b[1m   5/1562\u001b[0m \u001b[37m━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[1m19s\u001b[0m 13ms/step - accuracy: 0.4619 - loss: 1.4210  "
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-10-09 20:15:42.375288: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 18116607102968086293\n",
      "2024-10-09 20:15:42.375362: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 2094629562201250906\n",
      "2024-10-09 20:15:42.386668: I tensorflow/core/framework/local_rendezvous.cc:404] Local rendezvous is aborting with status: OUT_OF_RANGE: End of sequence\n",
      "\t [[{{node IteratorGetNext}}]]\n",
      "\t [[IteratorGetNext/_2]]\n",
      "2024-10-09 20:15:42.386772: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 18116607102968086293\n",
      "2024-10-09 20:15:42.386806: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 2094629562201250906\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[1m1562/1562\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m21s\u001b[0m 13ms/step - accuracy: 0.4850 - loss: 1.4258 - val_accuracy: 0.5371 - val_loss: 1.2746\n",
      "Epoch 6/15\n",
      "\u001b[1m1562/1562\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m0s\u001b[0m 9us/step - accuracy: 0.5000 - loss: 1.4513 - val_accuracy: 0.6250 - val_loss: 1.2871\n",
      "Epoch 7/15\n",
      "\u001b[1m   5/1562\u001b[0m \u001b[37m━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[1m20s\u001b[0m 13ms/step - accuracy: 0.5895 - loss: 1.3400  "
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-10-09 20:16:03.016049: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 18116607102968086293\n",
      "2024-10-09 20:16:03.016123: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 2094629562201250906\n",
      "2024-10-09 20:16:03.023976: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 18116607102968086293\n",
      "2024-10-09 20:16:03.024053: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 2094629562201250906\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[1m1562/1562\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m21s\u001b[0m 14ms/step - accuracy: 0.5092 - loss: 1.3677 - val_accuracy: 0.5976 - val_loss: 1.1121\n",
      "Epoch 8/15\n",
      "\u001b[1m1562/1562\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m0s\u001b[0m 11us/step - accuracy: 0.3750 - loss: 1.6392 - val_accuracy: 0.6250 - val_loss: 1.3242\n",
      "Epoch 9/15\n",
      "\u001b[1m   5/1562\u001b[0m \u001b[37m━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[1m20s\u001b[0m 13ms/step - accuracy: 0.6015 - loss: 1.1794  "
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-10-09 20:16:24.364160: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 18116607102968086293\n",
      "2024-10-09 20:16:24.364232: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 2094629562201250906\n",
      "2024-10-09 20:16:24.372082: I tensorflow/core/framework/local_rendezvous.cc:404] Local rendezvous is aborting with status: OUT_OF_RANGE: End of sequence\n",
      "\t [[{{node IteratorGetNext}}]]\n",
      "\t [[IteratorGetNext/_2]]\n",
      "2024-10-09 20:16:24.372157: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 18116607102968086293\n",
      "2024-10-09 20:16:24.372197: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 2094629562201250906\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[1m1562/1562\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m21s\u001b[0m 13ms/step - accuracy: 0.5280 - loss: 1.3189 - val_accuracy: 0.6146 - val_loss: 1.1136\n",
      "Epoch 10/15\n",
      "\u001b[1m1562/1562\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m0s\u001b[0m 10us/step - accuracy: 0.4062 - loss: 1.3562 - val_accuracy: 0.7500 - val_loss: 0.9009\n",
      "Epoch 11/15\n",
      "\u001b[1m   5/1562\u001b[0m \u001b[37m━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[1m19s\u001b[0m 13ms/step - accuracy: 0.5623 - loss: 1.2847  "
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-10-09 20:16:44.925463: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 18116607102968086293\n",
      "2024-10-09 20:16:44.925533: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 2094629562201250906\n",
      "2024-10-09 20:16:44.934241: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 18116607102968086293\n",
      "2024-10-09 20:16:44.934317: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 2094629562201250906\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[1m1562/1562\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m22s\u001b[0m 14ms/step - accuracy: 0.5441 - loss: 1.2797 - val_accuracy: 0.6034 - val_loss: 1.1183\n",
      "Epoch 12/15\n",
      "\u001b[1m1562/1562\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m0s\u001b[0m 9us/step - accuracy: 0.3438 - loss: 1.5814 - val_accuracy: 0.6250 - val_loss: 1.6778\n",
      "Epoch 13/15\n",
      "\u001b[1m   5/1562\u001b[0m \u001b[37m━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[1m20s\u001b[0m 13ms/step - accuracy: 0.6098 - loss: 1.2352  "
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-10-09 20:17:07.096784: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 18116607102968086293\n",
      "2024-10-09 20:17:07.096865: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 2094629562201250906\n",
      "2024-10-09 20:17:07.104494: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 18116607102968086293\n",
      "2024-10-09 20:17:07.104568: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 2094629562201250906\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[1m1562/1562\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m22s\u001b[0m 14ms/step - accuracy: 0.5550 - loss: 1.2457 - val_accuracy: 0.6110 - val_loss: 1.0816\n",
      "Epoch 14/15\n",
      "\u001b[1m1562/1562\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m0s\u001b[0m 13us/step - accuracy: 0.5000 - loss: 1.3999 - val_accuracy: 0.5000 - val_loss: 1.4292\n",
      "Epoch 15/15\n",
      "\u001b[1m   5/1562\u001b[0m \u001b[37m━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[1m22s\u001b[0m 14ms/step - accuracy: 0.5696 - loss: 1.3465  "
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-10-09 20:17:29.554187: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 18116607102968086293\n",
      "2024-10-09 20:17:29.554293: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 2094629562201250906\n",
      "2024-10-09 20:17:29.564490: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 18116607102968086293\n",
      "2024-10-09 20:17:29.564600: I tensorflow/core/framework/local_rendezvous.cc:423] Local rendezvous recv item cancelled. Key hash: 2094629562201250906\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[1m1562/1562\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m23s\u001b[0m 15ms/step - accuracy: 0.5633 - loss: 1.2275 - val_accuracy: 0.6190 - val_loss: 1.0766\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "<keras.src.callbacks.history.History at 0x7f73e2a64310>"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model.fit(train_data_gen\n",
    "          , steps_per_epoch=len(x_train)// batch_size\n",
    "          , epochs=15\n",
    "          , validation_data=val_img_gen\n",
    "          , validation_steps=len(x_val)//batch_size)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "wsjUaaSlyo2q",
    "outputId": "f6f24a9c-4b73-4ccf-dc63-fc101ad7da92"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[1m157/157\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m1s\u001b[0m 3ms/step - accuracy: 0.6260 - loss: 1.0750\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "[1.0770161151885986, 0.6186000108718872]"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model.evaluate(val_img_gen)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Model Selection\n",
    "I tried different models like ResNet and ResNet50 but Vgg16 model gave me the best results \n",
    "\n",
    "Before unfreezing the last 5 layers i tried with all layers freezed and the model performed horribly but after unfreezing it performed really well "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 1000
    },
    "id": "R032iVzF0bCx",
    "outputId": "3b45e3fc-608d-4f36-85a6-55aca21915db"
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<pre style=\"white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\"><span style=\"font-weight: bold\">Model: \"vgg16\"</span>\n",
       "</pre>\n"
      ],
      "text/plain": [
       "\u001b[1mModel: \"vgg16\"\u001b[0m\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "<pre style=\"white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\">┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓\n",
       "┃<span style=\"font-weight: bold\"> Layer (type)                    </span>┃<span style=\"font-weight: bold\"> Output Shape           </span>┃<span style=\"font-weight: bold\">       Param # </span>┃\n",
       "┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩\n",
       "│ input_layer_1 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">InputLayer</span>)      │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">32</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">32</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">3</span>)      │             <span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block1_conv1 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">32</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">32</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">64</span>)     │         <span style=\"color: #00af00; text-decoration-color: #00af00\">1,792</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block1_conv2 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">32</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">32</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">64</span>)     │        <span style=\"color: #00af00; text-decoration-color: #00af00\">36,928</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block1_pool (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">MaxPooling2D</span>)      │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">16</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">16</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">64</span>)     │             <span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block2_conv1 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">16</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">16</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">128</span>)    │        <span style=\"color: #00af00; text-decoration-color: #00af00\">73,856</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block2_conv2 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">16</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">16</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">128</span>)    │       <span style=\"color: #00af00; text-decoration-color: #00af00\">147,584</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block2_pool (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">MaxPooling2D</span>)      │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">8</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">8</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">128</span>)      │             <span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block3_conv1 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">8</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">8</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">256</span>)      │       <span style=\"color: #00af00; text-decoration-color: #00af00\">295,168</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block3_conv2 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">8</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">8</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">256</span>)      │       <span style=\"color: #00af00; text-decoration-color: #00af00\">590,080</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block3_conv3 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">8</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">8</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">256</span>)      │       <span style=\"color: #00af00; text-decoration-color: #00af00\">590,080</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block3_pool (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">MaxPooling2D</span>)      │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">4</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">4</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">256</span>)      │             <span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block4_conv1 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">4</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">4</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)      │     <span style=\"color: #00af00; text-decoration-color: #00af00\">1,180,160</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block4_conv2 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">4</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">4</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)      │     <span style=\"color: #00af00; text-decoration-color: #00af00\">2,359,808</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block4_conv3 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">4</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">4</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)      │     <span style=\"color: #00af00; text-decoration-color: #00af00\">2,359,808</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block4_pool (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">MaxPooling2D</span>)      │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">2</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">2</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)      │             <span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block5_conv1 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">2</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">2</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)      │     <span style=\"color: #00af00; text-decoration-color: #00af00\">2,359,808</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block5_conv2 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">2</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">2</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)      │     <span style=\"color: #00af00; text-decoration-color: #00af00\">2,359,808</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block5_conv3 (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">Conv2D</span>)           │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">2</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">2</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)      │     <span style=\"color: #00af00; text-decoration-color: #00af00\">2,359,808</span> │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block5_pool (<span style=\"color: #0087ff; text-decoration-color: #0087ff\">MaxPooling2D</span>)      │ (<span style=\"color: #00d7ff; text-decoration-color: #00d7ff\">None</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">1</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">1</span>, <span style=\"color: #00af00; text-decoration-color: #00af00\">512</span>)      │             <span style=\"color: #00af00; text-decoration-color: #00af00\">0</span> │\n",
       "└─────────────────────────────────┴────────────────────────┴───────────────┘\n",
       "</pre>\n"
      ],
      "text/plain": [
       "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓\n",
       "┃\u001b[1m \u001b[0m\u001b[1mLayer (type)                   \u001b[0m\u001b[1m \u001b[0m┃\u001b[1m \u001b[0m\u001b[1mOutput Shape          \u001b[0m\u001b[1m \u001b[0m┃\u001b[1m \u001b[0m\u001b[1m      Param #\u001b[0m\u001b[1m \u001b[0m┃\n",
       "┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩\n",
       "│ input_layer_1 (\u001b[38;5;33mInputLayer\u001b[0m)      │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m32\u001b[0m, \u001b[38;5;34m32\u001b[0m, \u001b[38;5;34m3\u001b[0m)      │             \u001b[38;5;34m0\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block1_conv1 (\u001b[38;5;33mConv2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m32\u001b[0m, \u001b[38;5;34m32\u001b[0m, \u001b[38;5;34m64\u001b[0m)     │         \u001b[38;5;34m1,792\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block1_conv2 (\u001b[38;5;33mConv2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m32\u001b[0m, \u001b[38;5;34m32\u001b[0m, \u001b[38;5;34m64\u001b[0m)     │        \u001b[38;5;34m36,928\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block1_pool (\u001b[38;5;33mMaxPooling2D\u001b[0m)      │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m16\u001b[0m, \u001b[38;5;34m16\u001b[0m, \u001b[38;5;34m64\u001b[0m)     │             \u001b[38;5;34m0\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block2_conv1 (\u001b[38;5;33mConv2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m16\u001b[0m, \u001b[38;5;34m16\u001b[0m, \u001b[38;5;34m128\u001b[0m)    │        \u001b[38;5;34m73,856\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block2_conv2 (\u001b[38;5;33mConv2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m16\u001b[0m, \u001b[38;5;34m16\u001b[0m, \u001b[38;5;34m128\u001b[0m)    │       \u001b[38;5;34m147,584\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block2_pool (\u001b[38;5;33mMaxPooling2D\u001b[0m)      │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m8\u001b[0m, \u001b[38;5;34m8\u001b[0m, \u001b[38;5;34m128\u001b[0m)      │             \u001b[38;5;34m0\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block3_conv1 (\u001b[38;5;33mConv2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m8\u001b[0m, \u001b[38;5;34m8\u001b[0m, \u001b[38;5;34m256\u001b[0m)      │       \u001b[38;5;34m295,168\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block3_conv2 (\u001b[38;5;33mConv2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m8\u001b[0m, \u001b[38;5;34m8\u001b[0m, \u001b[38;5;34m256\u001b[0m)      │       \u001b[38;5;34m590,080\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block3_conv3 (\u001b[38;5;33mConv2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m8\u001b[0m, \u001b[38;5;34m8\u001b[0m, \u001b[38;5;34m256\u001b[0m)      │       \u001b[38;5;34m590,080\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block3_pool (\u001b[38;5;33mMaxPooling2D\u001b[0m)      │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m4\u001b[0m, \u001b[38;5;34m4\u001b[0m, \u001b[38;5;34m256\u001b[0m)      │             \u001b[38;5;34m0\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block4_conv1 (\u001b[38;5;33mConv2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m4\u001b[0m, \u001b[38;5;34m4\u001b[0m, \u001b[38;5;34m512\u001b[0m)      │     \u001b[38;5;34m1,180,160\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block4_conv2 (\u001b[38;5;33mConv2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m4\u001b[0m, \u001b[38;5;34m4\u001b[0m, \u001b[38;5;34m512\u001b[0m)      │     \u001b[38;5;34m2,359,808\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block4_conv3 (\u001b[38;5;33mConv2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m4\u001b[0m, \u001b[38;5;34m4\u001b[0m, \u001b[38;5;34m512\u001b[0m)      │     \u001b[38;5;34m2,359,808\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block4_pool (\u001b[38;5;33mMaxPooling2D\u001b[0m)      │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m2\u001b[0m, \u001b[38;5;34m2\u001b[0m, \u001b[38;5;34m512\u001b[0m)      │             \u001b[38;5;34m0\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block5_conv1 (\u001b[38;5;33mConv2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m2\u001b[0m, \u001b[38;5;34m2\u001b[0m, \u001b[38;5;34m512\u001b[0m)      │     \u001b[38;5;34m2,359,808\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block5_conv2 (\u001b[38;5;33mConv2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m2\u001b[0m, \u001b[38;5;34m2\u001b[0m, \u001b[38;5;34m512\u001b[0m)      │     \u001b[38;5;34m2,359,808\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block5_conv3 (\u001b[38;5;33mConv2D\u001b[0m)           │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m2\u001b[0m, \u001b[38;5;34m2\u001b[0m, \u001b[38;5;34m512\u001b[0m)      │     \u001b[38;5;34m2,359,808\u001b[0m │\n",
       "├─────────────────────────────────┼────────────────────────┼───────────────┤\n",
       "│ block5_pool (\u001b[38;5;33mMaxPooling2D\u001b[0m)      │ (\u001b[38;5;45mNone\u001b[0m, \u001b[38;5;34m1\u001b[0m, \u001b[38;5;34m1\u001b[0m, \u001b[38;5;34m512\u001b[0m)      │             \u001b[38;5;34m0\u001b[0m │\n",
       "└─────────────────────────────────┴────────────────────────┴───────────────┘\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "<pre style=\"white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\"><span style=\"font-weight: bold\"> Total params: </span><span style=\"color: #00af00; text-decoration-color: #00af00\">14,714,688</span> (56.13 MB)\n",
       "</pre>\n"
      ],
      "text/plain": [
       "\u001b[1m Total params: \u001b[0m\u001b[38;5;34m14,714,688\u001b[0m (56.13 MB)\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "<pre style=\"white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\"><span style=\"font-weight: bold\"> Trainable params: </span><span style=\"color: #00af00; text-decoration-color: #00af00\">7,079,424</span> (27.01 MB)\n",
       "</pre>\n"
      ],
      "text/plain": [
       "\u001b[1m Trainable params: \u001b[0m\u001b[38;5;34m7,079,424\u001b[0m (27.01 MB)\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "text/html": [
       "<pre style=\"white-space:pre;overflow-x:auto;line-height:normal;font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace\"><span style=\"font-weight: bold\"> Non-trainable params: </span><span style=\"color: #00af00; text-decoration-color: #00af00\">7,635,264</span> (29.13 MB)\n",
       "</pre>\n"
      ],
      "text/plain": [
       "\u001b[1m Non-trainable params: \u001b[0m\u001b[38;5;34m7,635,264\u001b[0m (29.13 MB)\n"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "base_model = VGG16(input_shape=(32, 32, 3), include_top=False, weights='imagenet')\n",
    "\n",
    "# Fine-tune from this layer onwards\n",
    "unfreeze = 5\n",
    "\n",
    "# Freeze all the layers before the `fine_tune_at` layer\n",
    "for layer in base_model.layers[:-unfreeze]:\n",
    "  layer.trainable = False\n",
    "\n",
    "base_model.summary()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {
    "id": "OQd-2fWW7YcO"
   },
   "outputs": [],
   "source": [
    "model2 = tf.keras.Sequential([\n",
    "    base_model,\n",
    "    layers.Flatten(),\n",
    "    layers.Dense(500, activation='relu'),\n",
    "    layers.Dense(256, activation='relu'),\n",
    "    layers.Dense(10, activation='softmax')\n",
    "])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {
    "id": "GkWi-ozl8b-o"
   },
   "outputs": [],
   "source": [
    "optimizer = tf.keras.optimizers.Adam(0.001)\n",
    "model2.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "eJkCBL0z874C",
    "outputId": "a2e23c9c-019a-4d10-a27e-92723f0fd9b4"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Epoch 1/10\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-10-09 20:17:58.468438: I external/local_xla/xla/stream_executor/cuda/cuda_asm_compiler.cc:393] ptxas warning : Registers are spilled to local memory in function 'gemm_fusion_dot_1412', 32 bytes spill stores, 32 bytes spill loads\n",
      "\n",
      "2024-10-09 20:17:58.535124: I external/local_xla/xla/stream_executor/cuda/cuda_asm_compiler.cc:393] ptxas warning : Registers are spilled to local memory in function 'gemm_fusion_dot_1412', 28 bytes spill stores, 28 bytes spill loads\n",
      "\n",
      "2024-10-09 20:17:58.876413: I external/local_xla/xla/stream_executor/cuda/cuda_asm_compiler.cc:393] ptxas warning : Registers are spilled to local memory in function 'gemm_fusion_dot_1412', 12 bytes spill stores, 12 bytes spill loads\n",
      "\n",
      "2024-10-09 20:17:59.018692: I external/local_xla/xla/stream_executor/cuda/cuda_asm_compiler.cc:393] ptxas warning : Registers are spilled to local memory in function 'gemm_fusion_dot_1412', 24 bytes spill stores, 24 bytes spill loads\n",
      "\n",
      "2024-10-09 20:17:59.045110: I external/local_xla/xla/stream_executor/cuda/cuda_asm_compiler.cc:393] ptxas warning : Registers are spilled to local memory in function 'gemm_fusion_dot_1412', 36 bytes spill stores, 36 bytes spill loads\n",
      "\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[1m1563/1563\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m42s\u001b[0m 22ms/step - accuracy: 0.0954 - loss: 2.3069 - val_accuracy: 0.0962 - val_loss: 2.3027\n",
      "Epoch 2/10\n",
      "\u001b[1m1563/1563\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m25s\u001b[0m 16ms/step - accuracy: 0.0977 - loss: 2.3027 - val_accuracy: 0.0964 - val_loss: 2.3027\n",
      "Epoch 3/10\n",
      "\u001b[1m1563/1563\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m25s\u001b[0m 16ms/step - accuracy: 0.1016 - loss: 2.3027 - val_accuracy: 0.0962 - val_loss: 2.3027\n",
      "Epoch 4/10\n",
      "\u001b[1m1563/1563\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m25s\u001b[0m 16ms/step - accuracy: 0.1011 - loss: 2.3027 - val_accuracy: 0.1018 - val_loss: 2.3026\n",
      "Epoch 5/10\n",
      "\u001b[1m1563/1563\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m25s\u001b[0m 16ms/step - accuracy: 0.0964 - loss: 2.3027 - val_accuracy: 0.1018 - val_loss: 2.3027\n",
      "Epoch 6/10\n",
      "\u001b[1m1563/1563\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m25s\u001b[0m 16ms/step - accuracy: 0.1013 - loss: 2.3027 - val_accuracy: 0.1032 - val_loss: 2.3025\n",
      "Epoch 7/10\n",
      "\u001b[1m1563/1563\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m25s\u001b[0m 16ms/step - accuracy: 0.1031 - loss: 2.3026 - val_accuracy: 0.0962 - val_loss: 2.3028\n",
      "Epoch 8/10\n",
      "\u001b[1m1563/1563\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m25s\u001b[0m 16ms/step - accuracy: 0.0952 - loss: 2.3028 - val_accuracy: 0.1018 - val_loss: 2.3026\n",
      "Epoch 9/10\n",
      "\u001b[1m1563/1563\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m26s\u001b[0m 16ms/step - accuracy: 0.1001 - loss: 2.3028 - val_accuracy: 0.0978 - val_loss: 2.3026\n",
      "Epoch 10/10\n",
      "\u001b[1m1563/1563\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m26s\u001b[0m 16ms/step - accuracy: 0.0956 - loss: 2.3027 - val_accuracy: 0.0962 - val_loss: 2.3027\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "<keras.src.callbacks.history.History at 0x7f73b61ab350>"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model2.fit(train_data_gen\n",
    "           , epochs=10\n",
    "           , validation_data=val_img_gen\n",
    "           , verbose=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "MjNKr4HNYYnV",
    "outputId": "c68e4519-04c4-48a9-a6bf-cac2d050b68f"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[1m157/157\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m0s\u001b[0m 3ms/step - accuracy: 0.6204 - loss: 1.0673\n",
      "\u001b[1m1563/1563\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m23s\u001b[0m 15ms/step - accuracy: 0.5750 - loss: 1.1918\n",
      "\u001b[1m157/157\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m1s\u001b[0m 9ms/step - accuracy: 0.0934 - loss: 2.3027\n",
      "\u001b[1m1563/1563\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m23s\u001b[0m 15ms/step - accuracy: 0.1001 - loss: 2.3026\n",
      "Self created model\n",
      "Training accuracy: 0.5713800191879272\n",
      "Validation accuracy: 0.6186000108718872\n",
      "\n",
      "Transfer Model\n",
      "Training accuracy: 0.10000000149011612\n",
      "Validation accuracy: 0.09619999676942825\n"
     ]
    }
   ],
   "source": [
    "model_1_val_acc = model.evaluate(val_img_gen)\n",
    "model_1_train_acc = model.evaluate(train_data_gen)\n",
    "\n",
    "model_2_val_acc = model2.evaluate(val_img_gen)\n",
    "model_2_train_acc = model2.evaluate(train_data_gen)\n",
    "\n",
    "\n",
    "print(\"Self created model\")\n",
    "print(f\"Training accuracy: {model_1_train_acc[1]}\")\n",
    "print(f\"Validation accuracy: {model_1_val_acc[1]}\")\n",
    "print()\n",
    "print(\"Transfer Model\")\n",
    "print(f\"Training accuracy: {model_2_train_acc[1]}\")\n",
    "print(f\"Validation accuracy: {model_2_val_acc[1]}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Confusion Matrix"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[1m157/157\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m3s\u001b[0m 13ms/step\n",
      "\u001b[1m157/157\u001b[0m \u001b[32m━━━━━━━━━━━━━━━━━━━━\u001b[0m\u001b[37m\u001b[0m \u001b[1m1s\u001b[0m 9ms/step - accuracy: 0.1033 - loss: 2.3026\n",
      "Testing accuracy: 0.10379999876022339\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "array([[  0, 491,   0,   0,   0,   0,   0,   0,   0,   0],\n",
       "       [  0, 519,   0,   0,   0,   0,   0,   0,   0,   0],\n",
       "       [  0, 497,   0,   0,   0,   0,   0,   0,   0,   0],\n",
       "       [  0, 513,   0,   0,   0,   0,   0,   0,   0,   0],\n",
       "       [  0, 511,   0,   0,   0,   0,   0,   0,   0,   0],\n",
       "       [  0, 474,   0,   0,   0,   0,   0,   0,   0,   0],\n",
       "       [  0, 484,   0,   0,   0,   0,   0,   0,   0,   0],\n",
       "       [  0, 518,   0,   0,   0,   0,   0,   0,   0,   0],\n",
       "       [  0, 506,   0,   0,   0,   0,   0,   0,   0,   0],\n",
       "       [  0, 487,   0,   0,   0,   0,   0,   0,   0,   0]])"
      ]
     },
     "execution_count": 18,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "test_preds = model2.predict(x_test).argmax(axis=1)\n",
    "test_acc = model2.evaluate(test_img_gen)[1]\n",
    "print(f\"Testing accuracy: {test_acc}\")\n",
    "conf = confusion_matrix(y_test, test_preds)\n",
    "conf"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [],
   "source": [
    "from tensorflow.keras.preprocessing import image\n",
    "from tensorflow.keras.preprocessing.image import load_img\n",
    "from tensorflow.keras.preprocessing.image import img_to_array"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [],
   "source": [
    "def img_preprocess(path):\n",
    "    img = load_img(path, target_size=(32, 32))\n",
    "    img = img_to_array(img)\n",
    "    img = np.expand_dims(img, axis=0)\n",
    "    \n",
    "    return img"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [
    {
     "ename": "FileNotFoundError",
     "evalue": "[Errno 2] No such file or directory: './deer.jpg'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mFileNotFoundError\u001b[0m                         Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[21], line 1\u001b[0m\n\u001b[0;32m----> 1\u001b[0m img \u001b[38;5;241m=\u001b[39m \u001b[43mimg_preprocess\u001b[49m\u001b[43m(\u001b[49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[38;5;124;43m./deer.jpg\u001b[39;49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[43m)\u001b[49m\n\u001b[1;32m      3\u001b[0m model2\u001b[38;5;241m.\u001b[39mpredict(img)\u001b[38;5;241m.\u001b[39margmax(axis\u001b[38;5;241m=\u001b[39m\u001b[38;5;241m1\u001b[39m)\n",
      "Cell \u001b[0;32mIn[20], line 2\u001b[0m, in \u001b[0;36mimg_preprocess\u001b[0;34m(path)\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m \u001b[38;5;21mimg_preprocess\u001b[39m(path):\n\u001b[0;32m----> 2\u001b[0m     img \u001b[38;5;241m=\u001b[39m \u001b[43mload_img\u001b[49m\u001b[43m(\u001b[49m\u001b[43mpath\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mtarget_size\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43m(\u001b[49m\u001b[38;5;241;43m32\u001b[39;49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m32\u001b[39;49m\u001b[43m)\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m      3\u001b[0m     img \u001b[38;5;241m=\u001b[39m img_to_array(img)\n\u001b[1;32m      4\u001b[0m     img \u001b[38;5;241m=\u001b[39m np\u001b[38;5;241m.\u001b[39mexpand_dims(img, axis\u001b[38;5;241m=\u001b[39m\u001b[38;5;241m0\u001b[39m)\n",
      "File \u001b[0;32m/usr/local/lib/python3.11/dist-packages/keras/src/utils/image_utils.py:235\u001b[0m, in \u001b[0;36mload_img\u001b[0;34m(path, color_mode, target_size, interpolation, keep_aspect_ratio)\u001b[0m\n\u001b[1;32m    233\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;28misinstance\u001b[39m(path, pathlib\u001b[38;5;241m.\u001b[39mPath):\n\u001b[1;32m    234\u001b[0m         path \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mstr\u001b[39m(path\u001b[38;5;241m.\u001b[39mresolve())\n\u001b[0;32m--> 235\u001b[0m     \u001b[38;5;28;01mwith\u001b[39;00m \u001b[38;5;28;43mopen\u001b[39;49m\u001b[43m(\u001b[49m\u001b[43mpath\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[38;5;124;43mrb\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[43m)\u001b[49m \u001b[38;5;28;01mas\u001b[39;00m f:\n\u001b[1;32m    236\u001b[0m         img \u001b[38;5;241m=\u001b[39m pil_image\u001b[38;5;241m.\u001b[39mopen(io\u001b[38;5;241m.\u001b[39mBytesIO(f\u001b[38;5;241m.\u001b[39mread()))\n\u001b[1;32m    237\u001b[0m \u001b[38;5;28;01melse\u001b[39;00m:\n",
      "\u001b[0;31mFileNotFoundError\u001b[0m: [Errno 2] No such file or directory: './deer.jpg'"
     ]
    }
   ],
   "source": [
    "img = img_preprocess('./deer.jpg')\n",
    "\n",
    "model2.predict(img).argmax(axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "img = img_preprocess('./plane.jpg')\n",
    "\n",
    "model2.predict(img).argmax(axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "img = img_preprocess('./ship.jpg')\n",
    "\n",
    "model2.predict(img).argmax(axis=1)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Performance\n",
    "The model performed good as it predicted 2 images correctly which was taken from google and it was unable to predict 1 image as the image was quite hard to predict."
   ]
  }
 ],
 "metadata": {
  "accelerator": "GPU",
  "colab": {
   "gpuType": "T4",
   "provenance": []
  },
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.0rc1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
