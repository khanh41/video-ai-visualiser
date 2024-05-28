# Video AI Visualiser

## 1. Setup

- Create folder `triton/model_repository/label_detection/1`

- Download model `model.onnx` to folder above: https://drive.google.com/file/d/1VWoYOUS963sPTc68JYLuBZ2n48mlPvj7/view?usp=sharing

- Create file `config.pbtxt` in folder `triton/model_repository/label_detection` with the following content:

  ```text
  platform: "onnxruntime_onnx"
  max_batch_size: 0
  instance_group {
    name: "label_detection_group"
    count: 5
  }
  ```
  **where increase param `count` (worker) corresponding to server configuration to achieve best performance**

- Create `.env` file:

  ```text
  API_KEY=PMAK-664e0121dda89c0001f47b9d-d9b789d10ac702eeadaddea1c832b661d7
  ```

## 2. Deploy

```bash
docker compose up --build -d
```
