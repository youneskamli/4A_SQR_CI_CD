README des workflows:

Docker_push_GCR : Action déclenchée pour chaque tag semver pour utiliser le fichier Dockerfile pour créer et
pousser l’image de l’API avec en tag la version semver spécifiée. Le tag sera sous la forme : v*. * .*

newImage : Action déclenchée manuellement pour utiliser le fichier Dockerfile pour créer une image.

newPush : Action déclenchée à chaque changement pour builder l’application. Ceci est fait avec la fonction check_syntax.

![Docker push GCR](https://github.com/youneskamli/4A_SQR_CI_CD/actions/workflows/Docker_push_GCR.yml/badge.svg)

![newImage](https://github.com/youneskamli/4A_SQR_CI_CD/actions/workflows/newImage.yml/badge.svg)

![newPush](https://github.com/youneskamli/4A_SQR_CI_CD/actions/workflows/newPush.yml/badge.svg)
