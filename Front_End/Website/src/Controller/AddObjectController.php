<?php

/**
 * Contrôleur de la page d'ajout d'objet
 * Il s'agit d'une page de formulaire
 */

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Security\Core\Security;
use App\Entity\Article;
use App\Entity\ArticleUser;
use App\Entity\Links;
use App\Entity\ObjectRequest;
use App\Form\ObjectRequestType;


class AddObjectController extends AbstractController
{
    /**
     * @var Security
     */
    private $security; //On récupère les données de sécurité

    public function __construct(Security $security)
    {
        $this->security = $security;
    }

    /**
     * @Route("/add/object", name="object")
     */
    public function index(Request $request)
    {
        $article = new Article(); // On crée nos Objet
        $articleUser = new ArticleUser();
        $links = new Links();
        $objectRequested = new ObjectRequest();
        $user = $this->security->getUser(); // On récupère les données de l'utilisateur actuellement connecté

        $form = $this->createForm(ObjectRequestType::class, $objectRequested); // On crée notre formulaire
        $form->handleRequest($request); // On attends que l'utilisateur valide le formulaire

        /**
         * On vérifie que le formulaire est valide en fonction des valeurs entrées.
         * On défini nous même la variable ID qui est associée à l'utilisateur actuellement connecté.
         * On envoie enfin l'objet crée dans la BDD et on redirige l'utilisateur vers la page
         * d'affichage des listes.
         *
         * Notre objet objectRequested sert d'objet tampoin afin de n'avoir qu'un seul formulaire
         * One peut s'en servir comme d'historique de demande au final
         */
        if ($form->isSubmitted() && $form->isValid()) {
            $objectRequested->setUserId($user->getId());

            /**
             * Une fois la définition de notre objet tampon on peut
             * en reprendre les paramètres à ajouter dans la bdd
             */

            $article->setArticle($objectRequested->getArticle());

            $links->setLink($objectRequested->getLink());
            $links->setArticle($article);

            $articleUser->setUser($user);
            $articleUser->setArticle($article);
            $articleUser->setPrice($objectRequested->getPrice());

            $em = $this->getDoctrine()->getManager();
            $em->persist($objectRequested);
            $em->persist($article);
            $em->persist($links);
            $em->persist($articleUser);
            $em->flush();

            return $this->redirectToRoute('list');
        }
        return $this->render('add_object/index.html.twig', [
            'form' => $form->createView(),
        ]);
    }
}
