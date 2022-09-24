<?php

/**
 * Controlleur de la liste des objets
 * mis en alerte.
 * Permet de récuperer les objets dans la base de donnée en fonction de l'utilisateur
 * et de les mettre dans une liste qui sera affichée via twig
 */

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Security\Core\Security;
use App\Entity\Article;
use App\Entity\ArticleUser;
use Doctrine\Persistence\ManagerRegistry;


class ListController extends AbstractController
{
    /**
     * @var Security
     */
    private $security; // on récupère les données de connexion

    public function __construct(Security $security)
    {
        $this->security = $security;
    }

    /**
     * @Route("/list", name="list")
     */
    public function index(ManagerRegistry $doctrine): Response
    {
        $user = $this->security->getUser(); // On récupère l'utilisateur
        if ($user == null) {
            return $this->redirectToRoute('app_login'); // Si l'utilisateur n'est pas connecté alors on le renvoie vers la page de connexion
        } else {
            $id = $user->getId(); // On récupère l'ID de l'utilisateur
        }

        $repository = $doctrine->getRepository(ArticleUser::class); // On récupère les données de la BDD

        /**
         * On trie les données récupérées en fonction de l'ID de l'utilisateur
         * et par prix croissant
         */
        $product = $repository->findBy(
            ['user' => $user],
            ['price' => 'ASC'],
        );

        /**
         * On assemble les données pour obtenir un ensemble de clés valeurs
         * du type 'Nom de l'objet' => 'Prix'
         */
        $objects = [];
        for ($i = 0; $i < sizeof($product); $i++) {
            $duo =  [$product[$i]->getArticle()->getArticle() => [$product[$i]->getPrice(), $product[$i]->getId()]];
            $objects = array_merge($objects, $duo);
        }

        // var_dump($objects);
        /**
         * On renvoie enfin le tableau ainsi crée qui sera utilisé dans Twig
         */
        return $this->render('list/index.html.twig', [
            'objects' => $objects,
        ]);
    }
}
