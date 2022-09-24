<?php

/**
 * Classe permettant l'affichage d'un objet en fonction de son ID
 */

namespace App\Controller;

use Doctrine\Persistence\ManagerRegistry;
use Sensio\Bundle\FrameworkExtraBundle\Configuration\Method;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Security\Core\Security;
use App\Entity\Article;
use App\Entity\ArticleUser;
use App\Entity\Links;
use App\Form\LinksFormType;




class ObjectController extends AbstractController
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
     * @Route("/object/{id}", name="show_object")
     */
    public function show(Request $request, ManagerRegistry $doctrine, ArticleUser $product, int $id): Response
    {
        $user = $this->security->getUser(); // On récupère l'utilisateur
        if ($user == null) {
            return $this->redirectToRoute('app_login'); // Si l'utilisateur n'est pas connecté alors on le renvoie vers la page de connexion
        }

        $entityManager = $doctrine->getManager();
        $product = $entityManager->getRepository(ArticleUser::class)->find($id);
        /**
         * On vérifie que l'utilisateur a le droit d'acceder à l'objet
         * en comparant son ID avec l'ID de l'utilisateur qui a crée l'objet.
         * Si il n'a pas le droit, il est renvoyé vers sa liste.
         */
        if ($product->getUser() != $user) {
            return $this->redirectToRoute('list');
        }

        $newLink = new Links();
        $form = $this->createForm(LinksFormType::class, $newLink);
        $form->handleRequest($request);
        if ($form->isSubmitted() && $form->isValid()) {
            $newLink->setArticle($product->getArticle());
            $em = $this->getDoctrine()->getManager();
            $em->persist($newLink);
            $em->flush();

            return $this->redirect($request->getUri()); //Permet de rafraîchir la page
        }

        return $this->render('object/index.html.twig', [
            'objects' => $product->getArticle(),
            'price'   => $product->getPrice(),
            'links'   => $product->getArticle()->getLinks(),
            'form'    => $form->createView(),
        ]);
    }

    /**
     * Methode de suppression d'une alerte
     *
     * @Route("/object/delete/{id}")
     * @Method({"DELETE"})
     */
    public function delete(Request $request, $id)
    {
        $em = $this->getDoctrine()->getManager();
        $user = $this->security->getUser();
        $product = $em->getRepository(ArticleUser::class)->find($id);
        if ($product->getUser() != $user) {
            return $this->redirectToRoute('list');
        }
        $em->remove($product);
        $em->flush();
        return $this->redirectToRoute('list');
    }
}
