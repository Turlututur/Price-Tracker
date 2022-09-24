<?php

/**
 * Formulaire utilisé dans la page de détails d'un objet pour
 * lui ajouter un lien.
 */

namespace App\Form;

use App\Entity\Links;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;
use Symfony\Component\Form\Extension\Core\Type\TextType;

class LinksFormType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
        ->add('link', TextType::class, [
            'label' => 'Lien à ajouter',
            'help' => 'ex : https://www.amazon.fr/Mysocks%C2%AE-Plaine-Cheville-Chaussettes-Jaune/[...]'
        ]);
    }

    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            'data_class' => Links::class,
        ]);
    }
}
