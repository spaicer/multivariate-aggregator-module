"""Test the webserver built with FastAPI"""


from fastapi.testclient import TestClient
from .. import main
import pytest
import json

client = TestClient(main.app)

pytest.model_files = None

### Test LSTM auto-encoder

def test_multivariate_lstm_train():

    response = client.post(
        '/multivariate-lstm-train',
        json={
      "train_data": {
        "data": {
        "A1": [601.929 , 587.4339, 590.4059, 596.6575, 582.4339, 585.8266, 597.0676, 584.5786, 583.95  , 595.0085],
        "A2": [650.8372, 650.8372, 650.8372, 650.309 , 650.309 , 649.7221, 649.1147, 649.6167, 649.6167, 649.6167],
        "A3": [636.3697, 636.3697, 636.3697, 636.3697, 636.3697, 636.3697, 636.3697, 636.3697, 636.3697, 636.3697],
        "A4": [ 71.1788,  71.1788,  71.4192,  70.8146,  71.2311,  70.9744, 70.9744,  71.1484,  71.9672,  71.509 ],
        "A5": [ 36.9295,  36.9295,  37.1119,  36.722 ,  36.97  ,  36.8511, 36.8511,  36.9359,  37.4204,  37.1334]
        }
      },
      
      "paths": {
        "model": "keras_mvts_lstm.h5",
        "scaler": "mvts_scaler.gz"
      },
      "activation": "relu",
      "optimizer": "adam",
      "loss": "mae",
      "nb_epochs": 10,
      "batch_size": 64,
      "validation_split": 0.15,
      "initial_embeding_dim": 128,
      "patience": 1
    }
    )

    assert response.status_code == 200
    assert response.json() == {"dump_status": "model is saved successfully"}



def test_aggregate_multivariate_lstm_score():
   
    response = client.post(
        '/aggregate-multivariate-lstm-score',
        json= {
        "test_data": {
          "data": {
                  "A1": [580.7722, 592.1779, 587.5173, 583.7109, 594.7249, 604.5849, 611.5132, 616.7466, 608.9669, 597.9345],
                  "A2": [649.4124, 649.4124, 649.4124, 650.1096, 651.0769, 651.632 , 652.3653, 652.3653, 652.3653, 652.7337],
                  "A3": [636.3428, 636.3428, 636.3428, 635.6159, 635.6159, 635.9999, 635.9999, 635.9999, 636.6101, 636.6101],
                  "A4": [ 71.9601,  71.9601,  72.342 ,  73.5115,  74.2349,  73.8276, 73.5101,  73.2902,  72.4169,  72.7627],
                  "A5": [ 37.4148,  37.4148,  37.5577,  38.3091,  38.7071,  38.4878, 38.3124,  38.1843,  37.69  ,  37.8794]
          }
        },
        "paths": {
          "model": "keras_mvts_lstm.h5",
          "scaler": "mvts_scaler.gz"
        }
      }     
    )


    assert response.status_code == 200
    

### Test Vector Autoregression (VAR)
    
def test_best_multivariate_var_order():
    
    response = client.post(
        '/best-multivariate-var-order',
        json= {
          "train_data": {
            "data": {
            "A1": [581.8548, 593.3871, 606.7692, 617.4495, 607.2034, 611.0798, 608.6863, 612.1547, 616.4299, 613.6036, 612.7401],
            "A2": [650.3324, 653.4324, 656.5324, 660.4851, 664.025 , 667.125 , 670.225 , 673.325 , 675.7723, 678.1468, 670.2468],
            "A3": [636.0783, 639.2783, 642.4783, 645.6783, 648.8783, 652.0783, 655.8941, 659.2941, 662.6941, 666.0941, 657.4941],
            "A4": [ 71.5995,  75.4052,  78.4239,  81.2488,  84.4223,  87.5223, 90.167 ,  94.0031,  96.5254,  99.9436,  91.7232],
            "A5": [ 37.1851,  40.703 ,  43.803 ,  46.7039,  49.8039,  52.9039, 55.7653,  59.2997,  62.0945,  65.3581,  57.2736]
            }
          },
          "low_order": 1,
          "high_order": 5
        }     
    )

    
    assert response.status_code == 200
    assert response.json() == {
		  "best_order": 3
		}
    
    
    
    
def test_train_multivariate_var():
    
    response = client.post(
        '/train-multivariate-var',
        json= {
          "train_data": {
            "data": {
            "A1": [581.8548, 593.3871, 606.7692, 617.4495, 607.2034, 611.0798, 608.6863, 612.1547, 616.4299, 613.6036, 612.7401],
            "A2": [650.3324, 653.4324, 656.5324, 660.4851, 664.025 , 667.125 , 670.225 , 673.325 , 675.7723, 678.1468, 670.2468],
            "A3": [636.0783, 639.2783, 642.4783, 645.6783, 648.8783, 652.0783, 655.8941, 659.2941, 662.6941, 666.0941, 657.4941],
            "A4": [ 71.5995,  75.4052,  78.4239,  81.2488,  84.4223,  87.5223, 90.167 ,  94.0031,  96.5254,  99.9436,  91.7232],
            "A5": [ 37.1851,  40.703 ,  39.803 ,  46.7039,  49.8039,  52.9039, 55.7653,  59.2997,  62.0945,  65.3581,  57.2736]
            }
          },
            
          "paths": {
            "model": "mvts_var.joblib",
            "scaler": ""
          },
          "order": 3
        }
    )

    assert response.status_code == 200
		
def test_aggregate_multivariate_var():
   
    response = client.post(
        '/aggregate-multivariate-var',
        json= {
		  "test_data": {
			"data": {
			"A1": [594.1389, 603.7225, 592.7108, 586.646 , 581.9071, 594.399, 603.805 , 610.3627, 594.4159, 585.8747, 593.4889],
			"A2": [660.7306, 661.7306, 662.7306, 663.172, 649.172, 649.172, 649.7999, 649.7999, 649.7999, 650.5692, 651.0472],
			"A3": [648.6941, 649.8941, 651.0941, 652.2941, 636.4941, 636.4941, 636.4941, 636.4941, 636.4941, 636.4941, 636.4941],
			"A4": [82.9601,  83.9601,  85.2628,  86.1015,  72.6354,  72.267, 72.6729,  71.5571,  71.9891,  72.7238,  73.0851],
			"A5": [48.4208,  49.4208,  50.5938,  51.4909,  37.7824,  37.5984, 37.8305,  37.1935,  37.4089,  37.8443,  38.0595]
			}
		  },
		  "paths": {
			"model": "mvts_var.joblib",
			"scaler": ""
		  },
		  "order": 3
		}
    )

    assert response.status_code == 200
    
### Test PCA

def test_aggregate_multivariate_pca():
   
    response = client.post(
        '/aggregate-multivariate-pca',
        json= {
		  "test_data": {
			"data": {
			"A1": [594.1389, 603.7225, 592.7108, 586.646 , 581.9071, 594.399, 603.805 , 610.3627, 594.4159, 585.8747, 593.4889],
			"A2": [660.7306, 661.7306, 662.7306, 663.172, 649.172, 649.172, 649.7999, 649.7999, 649.7999, 650.5692, 651.0472],
			"A3": [648.6941, 649.8941, 651.0941, 652.2941, 636.4941, 636.4941, 636.4941, 636.4941, 636.4941, 636.4941, 636.4941],
			"A4": [82.9601,  83.9601,  85.2628,  86.1015,  72.6354,  72.267, 72.6729,  71.5571,  71.9891,  72.7238,  73.0851],
			"A5": [48.4208,  49.4208,  50.5938,  51.4909,  37.7824,  37.5984, 37.8305,  37.1935,  37.4089,  37.8443,  38.0595]
			}
		  },
		  "principal_component": 1
		} 
    )

    assert response.status_code == 200



# returns list of files in data/. 
def test_list_files():

    pytest.model_files = None

    response = client.get('/list-model-files')
    assert response.status_code==200, "Response Fail Reason: {}\n".format(response.reason)

    try:
        response_json = json.loads(response.text)
        pytest.model_files = response_json['files']
    except:
        assert False, "Key Error in the response data"


# remove files and directories in data/
def test_remove_files():

    response = client.post('/remove-model-files', json.dumps(pytest.model_files) )
    assert response.status_code==200, "Response Fail Reason: {}\n".format(response.reason)

