<?php
/**
 * On définie ici l'entitée 'ObjectRequest'.
 * Il s'agit d'un Objet auquel l'utilisateur souhaite recevoir un mail en cas de baisse de prix.
 * On écrira dans la bdd les paramètres entrés de cet objet
 * Cet objet représente une demande d'ajout d'objet dans la bdd et sert de tampon,
 * on en reprend les paramètres pour les ajouter dans la bdd principale,
 * la table crée sert d'historique de demande d'ajout d'objet.
 */

namespace App\Entity;

use App\Repository\ObjectRequestRepository;
use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity(repositoryClass=ObjectRequestRepository::class)
 */
class ObjectRequest
{
    /**
     * @ORM\Id
     * @ORM\GeneratedValue
     * @ORM\Column(type="integer")
     */
    private $id;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $article;

    /**
     * @ORM\Column(type="string", length=500)
     */
    private $link;

    /**
     * @ORM\Column(type="integer")
     */
    private $user_id;

    /**
     * @ORM\Column(type="float")
     */
    private $price;



    public function getId(): ?int
    {
        return $this->id;
    }

    public function getArticle(): ?string
    {
        return $this->article;
    }

    public function setArticle(string $article): self
    {
        $this->article = $article;

        return $this;
    }

    public function getLink(): ?string
    {
        return $this->link;
    }

    public function setLink(string $link): self
    {
        $this->link = $link;

        return $this;
    }

    public function getUserId(): ?int
    {
        return $this->user_id;
    }

    public function setUserId(int $user_id): self
    {
        $this->user_id = $user_id;

        return $this;
    }

    public function getPrice(): ?float
    {
        return $this->price;
    }

    public function setPrice(float $price): self
    {
        $this->price = $price;

        return $this;
    }
}
