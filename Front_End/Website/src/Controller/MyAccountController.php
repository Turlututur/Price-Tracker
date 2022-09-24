<?php

/**
 * Controlleur de la page de récapitulatif du compte
 */

namespace App\Controller;

use Sensio\Bundle\FrameworkExtraBundle\Configuration\Method;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Session\Session;
use Symfony\Component\Security\Core\Security;
use App\Entity\User;


class MyAccountController extends AbstractController
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
     * @Route("/my/account", name="my_account")
     */
    public function index(): Response
    {
        $user = $this->security->getUser(); // On récupère l'utilisateur
        if ($user == null) {
            return $this->redirectToRoute('app_login'); // Si l'utilisateur n'est pas connecté alors on le renvoie vers la page de connexion
        }
        return $this->render('my_account/index.html.twig', [
            'controller_name' => 'MyAccountController',
        ]);
    }

    /**
     * Methode permettant de supprimer un utilisateur,
     * il faut nettoyer la session avant de supprimer un utilisateur.
     * @Route("/account/delete/{id}")
     * @Method({"REMOVE"})
     */
    public function delete(Request $request, $id)
    {
        $em = $this->getDoctrine()->getManager();
        $user = $this->security->getUser();

        if ($user->getId() != $id) {
            return $this->redirectToRoute('list');
        } else {
            $em->remove($user);
            $em->flush();
            $session = $this->get('session');
            $session = new Session();
            $session->invalidate();
            return $this->redirectToRoute('homepage');
        }
    }
}
