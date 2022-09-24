<?php

/**
 * Permet la création du formulaire d'un Utilisateur
 */

namespace App\Form;

use App\Entity\User;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\EmailType;
use Symfony\Component\Form\Extension\Core\Type\PasswordType;
use Symfony\Component\Form\Extension\Core\Type\RepeatedType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\Extension\Core\Type\IntegerType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class UserType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options)
    {
        // On fabrique le formulaire
        $builder
            ->add('email', EmailType::class, [
                'label' => 'Adresse e-mail (*)',
                'help' => "ex: adresse@gmail.com",
            ])
            ->add('name', TextType::class, [
                'label' => 'Votre nom (*)',
                'help' => "ex: Bernard",
            ])
            ->add('password', RepeatedType::class, [
                'type' => PasswordType::class,
                'first_options' => ['label' => 'Mot de Passe (*)'],
                'second_options' => ['label' => 'Confirmer le mot de passe (*)']
            ])
            ->add('phoneNumber', IntegerType::class, [
                'required' => false,
                'help' => "ex: 0612345678",
                'label' =>'Numéro de téléphone (optionnel)'
            ])
        ;
    }

    public function configureOptions(OptionsResolver $resolver)
    {
        $resolver->setDefaults([
            'data_class' => User::class,
        ]);
    }
}
