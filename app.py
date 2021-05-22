from ui.form import UIForm


def main():
    app = UIForm()
    if app.token:
        app.show()


if __name__ == '__main__':
    main()
