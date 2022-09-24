<?php

/**
 * Entité Article, contient le nom d'un objet à placer en alerte
 * associé à un ID que l'on pourra lier à un Lien et un 
 * Utilisateur dans ArticleUser.
 */

namespace App\Entity;

use App\Repository\ArticleRepository;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity(repositoryClass=ArticleRepository::class)
 */
class Article
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
     * @ORM\OneToMany(targetEntity=Links::class, mappedBy="article", orphanRemoval=true)
     */
    private $links;

    /**
     * @ORM\OneToOne(targetEntity=ArticleUser::class, mappedBy="article", cascade={"persist", "remove"})
     */
    private $articleUser;

    public function __construct()
    {
        $this->links = new ArrayCollection();
    }

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

    /**
     * @return Collection<int, Links>
     */
    public function getLinks(): Collection
    {
        return $this->links;
    }

    public function addLink(Links $link): self
    {
        if (!$this->links->contains($link)) {
            $this->links[] = $link;
            $link->setArticle($this);
        }

        return $this;
    }

    public function removeLink(Links $link): self
    {
        if ($this->links->removeElement($link)) {
            // set the owning side to null (unless already changed)
            if ($link->getArticle() === $this) {
                $link->setArticle(null);
            }
        }

        return $this;
    }

    public function getArticleUser(): ?ArticleUser
    {
        return $this->articleUser;
    }

    public function setArticleUser(ArticleUser $articleUser): self
    {
        // set the owning side of the relation if necessary
        if ($articleUser->getArticle() !== $this) {
            $articleUser->setArticle($this);
        }

        $this->articleUser = $articleUser;

        return $this;
    }
}
