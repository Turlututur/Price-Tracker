<?php

/**
 * Formulaire de creation d'un objet tampon qui nous permet d'écrire les alertes
 * dans la base de données
 */

namespace App\Form;

use App\Entity\ObjectRequest;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\Extension\Core\Type\NumberType;

class ObjectRequestType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
            ->add('article', TextType::class, [
                'label' => "Nom de l'objet",
                'help' => 'ex : Chaussettes jaunes',
            ])
            ->add('link', TextType::class, [
                'label' => 'Lien',
                'help' => 'ex : https://www.amazon.fr/Mysocks%C2%AE-Plaine-Cheville-Chaussettes-Jaune/[...]'
            ])
            ->add('price', NumberType::class, [
                'label' => 'Prix (€)',
                'help' => 'ex : 15.99',
                'scale' => 2,
            ])
        ;
    }

    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults([
            'data_class' => ObjectRequest::class,
        ]);
    }
}
