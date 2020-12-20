import logging
import os
import gphoto2 as gp


def imgcap():
    logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    callback_obj = gp.check_result(gp.use_python_logging())
    camera = gp.Camera()
    camera.init()
    print('Capturing image')
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
    print(f'Camera file path: {file_path.folder}/{file_path.name}')
    cwd = os.path.join(os.getcwd(), 'fromCamera')
    print(cwd)

    target = os.path.join(cwd, file_path.name)
    print('Copying image to', target)
    camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
    camera_file.save(target)
    camera.exit()


def imgcaps(i):
    logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    callback_obj = gp.check_result(gp.use_python_logging())
    camera = gp.Camera()
    camera.init()
    for j in range(i):
        print(f'Capturing image:{j + 1}')

        file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
        print(f'Camera file path: {file_path.folder}/{file_path.name}')

        cwd = os.path.join(os.getcwd(), 'fromCamera')
        print(cwd)

        target = os.path.join(cwd, file_path.name)
        print(f'Copying image {j + 1} : to', target)
        camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
        camera_file.save(target)
    camera.exit()
    print('done')
    # return 0


imgcaps(1)
